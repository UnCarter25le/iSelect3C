# -*- coding:utf-8 -*-
"""
程式名稱：以『關鍵搜索字』爬蟲pchome。
程式描述：

    1. 指定 searchword ，就可以在pchome 三個分類上(24h、購物中心、代購服務)查詢，每個分類最多回應2000筆。

    2. 關鍵字 冷暖空調 從24h上取得資料，一共有 62 頁， 1231筆。
        關鍵字 冷暖空調 從vdr上取得資料，一共有 70 頁， 1400筆。
        關鍵字 冷暖空調 從kdn上取得資料，一共有 100 頁， 3880筆。
    
    多進程，估計共耗時：998.5998482704163 秒  5/29/2019

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
from libs.multiProcessing import distributeKeyword
from libs.time import timeSleepEight
from libs.time import timeSleepRandomly
from libs.time import timeSleepTwo
from libs.time import timeSleepOne

def getPageFirst(keyword, searchword, headers):
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

# 進程worker不能有關鍵字引數、以及**kwargs
# 在terminal執行多進程，原本的output.put()  input.get() 的output input，都換成建立的mp.JoinableQueue()
def getPageInARow(input, searchword, headers, objectiveFolder, objective, *args):
    begin = time.time()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        keyword = input.get()
        print("getPageInARow is in new process %s, %s " % (getPageInARow_proc, thisPID))
        eraseRawData(objectiveFolder, objective, searchword, keyword=keyword)
        mkdirForRawData(objectiveFolder, objective, searchword, keyword=keyword)

        totalPage, totalRows = getPageFirst(keyword, searchword, headers)

        print(f"關鍵字 {searchword} 從{keyword}上取得資料，一共有 {totalPage} 頁， {totalRows}筆。")
        # countRaws += int(totalRows)
        # countPages += int(totalPage)

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
        print(f"這裡是getPageInARow_{thisPID}，準備完成工作。 ")
        print()
        end = time.time()
        print('getPageInARow 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()  #通知main process此次的input處理完成！
        timeSleepOne() #暫停幾秒來模擬現實狀況。



if __name__ == '__main__':

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
               "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}

    objectiveFolder = "rawData"

    objective = "pchome"

    searchword = "冷暖空調"

    begin = time.time()
    print('start in main process %s' %os.getpid())

    # 共同佇列宣告
    keyword_queue = mp.JoinableQueue()

    # 啟動行程
    Process_1 = []
    for p in range(3):
        getPageInARow_proc = mp.Process(target=getPageInARow, args=(keyword_queue, searchword, headers, objectiveFolder, objective,))#*args
        getPageInARow_proc.daemon = True
        getPageInARow_proc.start()
        print(f'建立第{p}個 getPageInARow_proc, {os.getpid()}, {getPageInARow_proc}')
        Process_1.append(getPageInARow_proc)


    # 主行程    
    keywordList = ["24h", "vdr", "kdn"]# 24小時、購物中心、代購服務

    distributeKeyword(keywordList, keyword_queue)


    keyword_queue.join()
    # for proc in process:
    #     proc.join()
    
    print('Function getPageInARow has done all jobs!')
    
    
    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')

    end = time.time()
    # print(f"關鍵字 {searchword} 從24h、購物中心、代購服務上取得資料，一共有 {countPages} 頁， {countRaws}筆。")
    print("完成！一共耗時：{0} 秒".format(end-begin)) 

