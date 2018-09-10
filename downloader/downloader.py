# coding:utf-8
from helper import proxyhelper, loghelper, db, filehelper
import requests
from urllib.parse import urlparse
from selenium import webdriver

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'Cookie':'ASPSESSIONIDAQSASCQC=OPJBPIIBCCJPPNKDEJCBNIMH; __51cke__=; Hm_lvt_8fd158bb3e69c43ab5dd05882cf0b234=1536294538,1536318190,1536324616,1536367606; ASPSESSIONIDASSBRDQD=NEEJPPIBLEGAJMDBLKFLIFAG; ASPSESSIONIDASRDTCRD=DBBKBMKBJCLKNDGFGGHCLNOP; ASPSESSIONIDCSQARCRC=BDIBCDLBGAJHKIJLGCENOHAK; acw_tc=781bad2215363877038416993e6e7d0c1a3969e2ff3dd4ec609aef516bbcf1; __tins__16949115=%7B%22sid%22%3A%201536386585775%2C%20%22vd%22%3A%2021%2C%20%22expires%22%3A%201536389932100%7D; __51laig__=51; Hm_lpvt_8fd158bb3e69c43ab5dd05882cf0b234=1536388132',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
           }
chromeOptions = webdriver.ChromeOptions()


def _default_is_html_valid(html):
    return '<htm' in html


def download(url, is_html_valid=_default_is_html_valid, auto_protocol=False, use_selenium=False, use_proxy=True, timeout=5, thread_id=-1):
    html = None
    if use_selenium:
        while True:
            if use_proxy:
                proxy = proxyhelper.next()
                chromeOptions.add_argument("--window-position=10000,10000 --proxy-server=" + proxy['proxy_addr'])

            browser = webdriver.Chrome(chrome_options=chromeOptions)
            browser.get(url)
            html = browser.page_source
            if is_html_valid(html):
                break
            else:
                continue
        browser.close()
    else:
        headers['Host'] = urlparse(url).hostname
        proxy = None
        response = None
        while True:
            try:
                if use_proxy:
                    proxy = proxyhelper.next(urlparse(url).scheme, thread_id)
                    response = requests.get(url, headers=headers, proxies={proxy['protocol']: proxy['proxy_addr']}, timeout=timeout)
                else:
                    response = requests.get(url, headers=headers, timeout=timeout)
                html = response.text
                if is_html_valid(html):
                    proxyhelper.reback(proxy, proxyhelper.status_succeed, thread_id=thread_id)
                    break
                else:
                    loghelper.error(url + ' -> is_html_valid=false')
                    loghelper.error(html)
                    proxyhelper.reback(proxy, proxyhelper.status_unknown, thread_id=thread_id)
                    continue
            except Exception as msg:
                proxyhelper.reback(proxy, proxyhelper.status_failed, thread_id=thread_id)
                print(str(msg))
                continue
        # end while
    return html
