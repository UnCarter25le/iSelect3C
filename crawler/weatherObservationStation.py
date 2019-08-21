# -*- coding:utf-8 -*-
"""
程式名稱：
程式描述：

    1. 

    2. 

備　　註：

#
http://e-service.cwb.gov.tw/HistoryDataQuery/

"""

from bs4 import BeautifulSoup
import requests
import os
import sys
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 專案資料夾下第二層，用兩個path.dirname
sys.path.append(_BASE_PATH)

from libs.splinterBrowser import buildSplinterBrowser
from libs.splinterBrowser import browserWaitTime
from libs.timeWidget import timeCalculate
from libs.timeWidget import timeStampGenerator
from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData



if __name__ == '__main__':

    objectiveFolder = "rawData"

    objective = "observationStation"

    begin = timeCalculate()

    browser = buildSplinterBrowser("chrome")
    browserWaitTime(browser)

    browser.visit("http://e-service.cwb.gov.tw/HistoryDataQuery/")

    #等待地圖的JS出來
    browser.is_element_present_by_xpath('//*[@id="con_r"]/div/div[1]', wait_time=5)

    soup = BeautifulSoup(browser.html,"html.parser")

    browser.quit()
    print("==============================quit==============================")

    eraseRawData(objectiveFolder, objective, "overviewData")
    mkdirForRawData(objectiveFolder, objective, "overviewData")

    timeStamp = timeStampGenerator()

    with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/overviewData/observation_{timeStamp}.txt", 'w', encoding='utf-8')as f:
        f.write(str(soup))
    
    print(f"成功寫出  observation_{timeStamp}.txt")


    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))







