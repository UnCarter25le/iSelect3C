# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。

from bs4 import BeautifulSoup
import requests
import random
import os
import sys

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module


_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}


def proxiesIpGenerator():
    """
    check the ip address we carry : http://ip.filefab.com/index.php
    proxy ips for reference : https://cn-proxy.com/
    """
    proxy_ips = ['124.156.108.71:82', '60.217.143.23:8060', '116.114.19.204:443']
    proxy_ip = random.Choice(proxy_ips)
    res = requests.get(url, headers=headers, proxies = {"http": "http://"+proxy_ip })

    print('Use', ip)
    resp = requests.get('http://ip.filefab.com/index.php',
                        proxies={'http': 'http://' + ip})
    soup = BeautifulSoup(resp.text, 'html.parser')
    print(soup.find('h1', id='ipd').text.strip())
    
        