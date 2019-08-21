# -*- coding:utf-8 -*-
"""
程式名稱：以『關鍵搜索字』爬蟲pchome。
程式描述：

    1. 指定 searchword ，就可以在pchome 三個分類上(24h、購物中心、代購服務)查詢，每個分類最多回應2000筆。
    
    2. 關鍵字 冷暖空調 從24h上取得資料，一共有 62 頁， 1231筆。
        關鍵字 冷暖空調 從vdr上取得資料，一共有 70 頁， 1400筆。
        關鍵字 冷暖空調 從kdn上取得資料，一共有 100 頁， 3880筆。
    
    單進程，估計共耗時：2276.9443397521973 秒  5/29/2019

備　　註：

    需要捕捉的欄位：
    "pics"、"picb"、"name"、originprice"、"Id"、"produrl"

    以關鍵字「冷暖空調」在pchomeAPI的三個分類做查詢的品項是4388，還未把非真正冷氣空調的去掉。

"""

from bs4 import BeautifulSoup
import requests
import json
# import re
# import csv
import os
# import shutil #high level os
import sys
import time
# import random
import multiprocessing as mp

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.timeWidget import timeSleepEight
from libs.timeWidget import timeSleepRandomly
from libs.timeWidget import timeSleepTwo


def getPageFirst(keyword, searchword):
    global headers
    url = "https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page=1&sort=sale/dc".format(keyword, searchword)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    try:
        jsonPage = json.loads(res.text)
        totalPage = jsonPage['totalPage']
        totalRows = jsonPage['totalRows']
        timeSleepTwo()
        return totalPage, totalRows
    except Exception as e:
        print("getPageFirst這裡發生錯誤   "+str(e)+"正在處理中。")
        timeSleepEight()
        jsonPage = json.loads(res.text)
        totalPage = jsonPage['totalPage']
        totalRows = jsonPage['totalRows']
        timeSleepTwo()
        return totalPage, totalRows


def getPageInARow(keyword, searchword, totalPage, totalRows):
    global headers

    for page in range(1, totalPage+1):
        url = 'https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc'.format(keyword, searchword, page)
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'

        timeSleepRandomly()

        try:
            jsonPage = json.loads(res.text)
            with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/{keyword}/{page}_{totalPage}_{totalRows}_{keyword+searchword}.json", 'w', encoding='utf-8')as f:
                json.dump(jsonPage, f, indent=2, ensure_ascii=False)
            print("成功寫出  {0}  第{1}頁".format(keyword+searchword, page))
            timeSleepEight()

        except Exception as e:
            print("getPageInARow這裡發生錯誤   "+str(e)+"正在處理中。")
            timeSleepEight()
            jsonPage = json.loads(res.text)
            with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/{keyword}/{page}_{totalPage}_{totalRows}_{keyword+searchword}.json", 'w', encoding='utf-8')as f:
                json.dump(jsonPage, f, indent=2, ensure_ascii=False)
            print("成功寫出  {0}  第{1}頁".format(keyword+searchword, page))
            timeSleepEight()


if __name__ == '__main__':

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
               "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}

    objectiveFolder = "rawData"

    objective = "pchome"

    searchword = "冷暖空調"

    begin = time.time()

    countRaws = 0
    countPages = 0

    for keyword in ["24h", "vdr", "kdn"]:# 24小時、購物中心、代購服務
        
        eraseRawData(objectiveFolder, objective, searchword, keyword=keyword)

        mkdirForRawData(objectiveFolder, objective, searchword, keyword=keyword)

        totalPage, totalRows = getPageFirst(keyword, searchword)

        print(f"關鍵字 {searchword} 從{keyword}上取得資料，一共有 {totalPage} 頁， {totalRows}筆。")
        countRaws += int(totalRows)
        countPages += int(totalPage)

        getPageInARow(keyword, searchword, totalPage, totalRows)

    end = time.time()
    print(f"關鍵字 {searchword} 從24h、購物中心、代購服務上取得資料，一共有 {countPages} 頁， {countRaws}筆。")
    print("完成！一共耗時：{0} 秒".format(end-begin)) 
