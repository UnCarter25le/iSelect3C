# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os
import sys
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.time import timeSleepRandomly



def buildSplinterBrowser(browserName):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # capabilities = dict(DesiredCapabilities.CHROME)
    # capabilities["acceptCerts"] = True
    # capabilities["acceptInsecureCerts"] = True
    browser = Browser(driver_name = browserName, headless=False, incognito=True)#, options = chrome_options)
#     cookies = {'_gat_gtag_UA_22652017_1': '1',
#                '_gid': 'GA1.3.515977689.1556715819',
#                '__auc': '4c27a68a16a737e4e8e40595d79',
#                '__asc': '4c27a68a16a737e4e8e40595d79',
#                '_atrk_siteuid': 'szryrpMZNv_2dxf1',
#                'appier_page_isView_ERlDyPL9yO7gfOb': 'b0eb3db6fc8ba926123b924e84ad8ef0901cb6c4cf85053fc1277a321c8b6d5d',
#                'appier_pv_counterERlDyPL9yO7gfOb': '0',
#                '_ga': 'GA1.3.1031198319.1556715819',
#                '_fbp': 'fb.3.1556715818686.1652118424',
#                '_atrk_ssid': 'asp7X5nELZJmt0w9NaDTUV',
#                'NSC_MC_TTP_WT': 'ffffffffc3a02ac945525d5f4f58455e445a4a4229a0',
#                '_atrk_sessidx': '1',
#                'appier_utmz': '%7B%7D',
#                '__BWfp': 'c1556715818782xb4d1f021b',
#                'JSESSIONID': '6A7C0B62A1C6E8D61ED7E723B4D725E5-m1.shop33',
#                'NSC_MC-xxx.npnptipq.dpn.ux*80': 'ffffffff0934543045525d5f4f58455e445a4a4229a0'}
#     browser.cookies.add(browser.cookies.all())
    return browser

def buildSplinterBrowserHeadless(browserName):
    browser = Browser(driver_name = browserName, headless=False, incognito=True)
    return browser


def browserWaitTime(browser):
    browser.wait_time
    timeSleepRandomly()

# scheme of making object
# class bbb(object):
#     def __init__(self,num):
#         self.num = num
#     def buildSplinterBrowser(self, browserName):
#         browser = Browser(driver_name = browserName, headless=False, incognito=True)#, options = chrome_options)
#         return browser

# browser = BBB.buildSplinterBrowser("chrome")

# browser.visit("https://www.google.com/")