# coding:utf-8
from helper import proxyhelper, loghelper
import requests
from urllib.parse import urlparse
from selenium import webdriver

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
           }
chromeOptions = webdriver.ChromeOptions()


def _default_is_html_valid(html):
    return '<htm' in html


def _download_use_selenium(url, is_html_valid=_default_is_html_valid, use_proxy=True, timeout=10):
    while True:
        try:
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
        except Exception as ex:
            browser.close()


def download(url, is_html_valid=_default_is_html_valid, auto_protocol=False, use_selenium=False, use_proxy=True, timeout=10):
    if use_selenium:
        return _download_use_selenium(url, is_html_valid, use_proxy, timeout)
    else:
        headers['Host'] = urlparse(url).hostname
        while True:
            try:
                if use_proxy:
                    proxy = proxyhelper.next(urlparse(url).scheme)
                    print(proxy)
                    response = requests.get(url, headers=headers, proxies={proxy['protocol']: proxy['proxy_addr']}, timeout=timeout)
                else:
                    response = requests.get(url, headers=headers, timeout=timeout)
                html = response.text
                if is_html_valid(html):
                    break
                else:
                    loghelper.error(url + ' -> is_html_valid=false')
                    continue
            except Exception as msg:
                print(str(msg))
                continue
        # end while
        return html
