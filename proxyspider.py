import requests
from bs4 import BeautifulSoup
from helper import db
import time
from selenium import webdriver
from urllib.parse import urlparse

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
           }

'''
ttps://free-proxy-list.net/
http://www.xicidaili.com/
http://www.89ip.cn/
http://www.ip3366.net/?stype=1&page=
'''


def execute():
    proxy_spiders = [# proxy_spider_free_proxy_list,
                     proxy_spider_xicidaili,
                     proxy_spider_89ip,
                     proxy_spider_ip3366,
                     proxy_spider_goubanjia,
                     proxy_spider_66ip
                     ]
    for proxy_spider in proxy_spiders:
        try:
            proxy_spider()
        except Exception as msg:
            print(msg)


def proxy_spider_xicidaili():
    soup = get_soup('http://www.xicidaili.com/')
    for tr in soup.select('#ip_list  tr'):
        tds = tr.select('td');
        if len(tds) == 8 and (tds[5].text == 'HTTP' or tds[5].text == 'HTTPS'):
            ip = tds[1].text
            port = tds[2].text
            protocol = tds[5].text.strip().lower()
            proxy_addr = protocol + '://' + ip + ':' + port
            try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol, 'proxy_addr': proxy_addr, 'usability': 0})


def proxy_spider_89ip():
    soup = get_soup('http://www.89ip.cn/')
    for tr in soup.select('body  div.layui-row.layui-col-space15 > div.layui-col-md8 > div > div.layui-form > table > tbody > tr'):
        tds = tr.select('td');
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        protocol = 'http'
        proxy_addr = protocol + '://' + ip + ':' + port
        try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol, 'proxy_addr': proxy_addr, 'usability': 0})
        protocol = 'https'
        proxy_addr = protocol + '://' + ip + ':' + port
        try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol, 'proxy_addr': proxy_addr, 'usability': 0})


def proxy_spider_free_proxy_list():
    soup = get_soup('https://free-proxy-list.net/')
    for tr in soup.select('#proxylisttable tr')[1:]:
        ip = tr.select('td')[0].text
        port = tr.select('td')[1].text
        protocol = 'http' if tr.select('td')[6].text.strip() == 'no' else 'https'
        proxy_addr = protocol + '://' + ip + ':' + port
        try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol, 'proxy_addr': proxy_addr, 'usability': 0})


def proxy_spider_ip3366():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--window-position=10000,10000 ")
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    headers['Host'] = 'www.ip3366.net'
    for page in range(3):  # 10
        url = 'http://www.ip3366.net/?stype=1&page=' + str(page + 1)
        print('spider:' + url)
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for tr in soup.select('#list > table > tbody > tr'):
            tds = tr.select('td')
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            protocol = tds[3].text.strip().lower()
            proxy_addr = protocol + '://' + ip + ':' + port
            try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol, 'proxy_addr': proxy_addr, 'usability': 0})
        time.sleep(10)
    browser.close()


def try_add_proxies(proxy):
    proxy['usability'] = 0
    proxy['proxy_addr'] = proxy['protocol'] + '://' + proxy['ip'] + ':' + proxy['port']
    if db.proxies.find_one({'proxy_addr': proxy['proxy_addr']}) is None:
        print('add proxy:' + proxy['proxy_addr'])
        db.proxies.insert_one(proxy)


def get_soup(url):
    print('spider:' + url)
    headers['Host'] = urlparse(url).hostname
    html = requests.get(url, headers=headers).text
    return BeautifulSoup(html, 'html.parser')


def proxy_spider_66ip():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--window-position=10000,10000 ")
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    headers['Host'] = 'www.ip3366.net'
    for page in range(1, 2):  # 400
        url = 'http://www.66ip.cn/{}.html'.format(page)
        print('spider:{}'.format(url))
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for tr in soup.select('#main > div > div:nth-of-type(1) > table > tbody > tr')[1:]:
            tds = tr.select('td')
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            protocol = 'http'
            try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol})
            protocol = 'https'
            try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol})


def proxy_spider_goubanjia():
    soup = get_soup('http://www.goubanjia.com/')
    for tr in soup.select('#services > div > div.row > div > div > div > table > tbody > tr'):
        tds = tr.select('td')
        ip = ''
        port = ''
        for t in tds[0].select('*'):
            if 'style' in t.attrs and 'none;' in t.attrs['style']:
                continue
            if 'class' in t.attrs and 'port' in t.attrs['class']:
                port = t.text.strip()
            else:
                ip += t.text.strip()
        protocol = tds[2].text.strip()
        try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol})


def proxy_spider_zdaye():
    from helper import proxyhelper
    import re

    # def get_usable_proxy_addr():
    #     while True:
    #         try:
    #             proxy = proxyhelper.next('http')
    #             baidu_html = requests.get('http://www.baidu.com', proxies={'http': proxy['proxy_addr']}, timeout=3).text
    #             return proxy['proxy_addr']
    #         except Exception as msg:
    #             print(msg)
    #
    # def fetch_html(url):
    #     global browser
    #     while True:
    #         chromeOptions = webdriver.ChromeOptions()
    #         # chromeOptions.add_argument("--proxy-server=" + get_usable_proxy_addr())
    #         # chromeOptions.add_argument('--window-position=10000,10000')
    #         browser = webdriver.Chrome(chrome_options=chromeOptions)
    #         browser.get(url)
    #         html = browser.page_source
    #
    #         if 'ERROR: Forbidden' in html or '404 Not Found' in html or '无法访问此网站' in html or '因为大部分的IP数据是过期的' in html or '<html' not in html:
    #             continue
    #         return html

    for page_index in range(53, 610):
        try:
            print('page={0}'.format(page_index))
            chromeOptions = webdriver.ChromeOptions()
            for header_key in headers:
                chromeOptions.add_argument('{}={}'.format(header_key, headers[header_key]))
            browser = webdriver.Chrome(chrome_options=chromeOptions)
            browser.set_page_load_timeout(20)
            url = 'http://ip.zdaye.com/dayProxy/{}.html'.format(page_index)
            browser.get(url)
            time.sleep(10)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.select('.ips > .title > a'):
                try:
                    browser.find_element_by_link_text(a.get_text()).click()
                    time.sleep(10)
                except Exception as msg:
                    print(msg)
                    browser.get(url)
                    time.sleep(10)
                    continue
                html1 = browser.page_source
                soup1 = BeautifulSoup(html1, 'html.parser')
                _str = soup1.select_one('.cont').get_text()
                _regex = '\d+\.\d+\.\d+\.\d+:\d+@HTTPS{0,1}'
                proxies_text = re.findall(_regex, _str)
                for proxy_text in proxies_text:
                    ip = proxy_text.split(':')[0]
                    port = proxy_text.split(':')[1].split('@')[0]
                    protocol = proxy_text.split(':')[1].split('@')[1].lower()
                    proxy_addr = protocol + '://' + ip + ':' + port
                    try_add_proxies({'ip': ip, 'port': port, 'protocol': protocol})
                browser.back()
                time.sleep(10)
            browser.close()
            time.sleep(10)
        except Exception as msg:
            browser.close()
            print(msg)
            continue


def proxy_spider_zdaye1():
    url = 'http://ip.zdaye.com/dayProxy/2018/9/1.html'
    chromeOptions = webdriver.ChromeOptions()
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser.get(url)
    html = browser.page_source


#  proxy_spider_zdaye()

while True:
    execute()
    time.sleep(60)
