# -*- coding:utf-8 -*-

"""
程式名稱：以『關鍵搜索字』爬蟲momo。
程式描述：

    1. 完成 keywordUrlPair ，就可以在momo 上以『searchType 3價格高至低』爬蟲。
    
    2. python必須啟動瀏覽器才能『看到』momo的產品頁。


備　　註：

    需要捕捉的欄位：
    "pics"、"picb"（設為None）、"name"、originprice"、"Id"、"produrl"



#2018-3-15   如果在執行splinter時，出現以下錯誤，下載最新的chromedriver，可以解決
Message: chrome not reachable (Session info: chrome=65.0.3325.146) 
(Driver info: chromedriver=2.33.506092 (733a02544d189eeb751fe0d7ddca79a0ee28cce4),platform=Linux 4.13.0-36-generic x86_64)


30個process
完成！一共耗時：925.360677242279 秒

"""

from bs4 import BeautifulSoup
import requests
import json
import re
import csv
import os
# import shutil #high level os
import sys
# import time
# import random
import signal
# from math import ceil
import multiprocessing as mp
# from urllib3.exceptions import MaxRetryError
# from urllib3.exceptions import NewConnectionError
from selenium.common.exceptions import TimeoutException

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)

from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.time import timeSleepRandomly
from libs.time import timeSleepEight
from libs.time import timeSleepOne
from libs.time import timeSleepTwo
from libs.time import timeSleepFour
from libs.time import timeCalculate
from libs.multiProcessing import distributeKeyword
from libs.multiProcessing import _momoKeywordUrlPair
from libs.manipulateDir import initialFile
from libs.regex import searchNums
from libs.regex import interDiv
from libs.splinterBrowser import buildSplinterBrowserHeadless
from libs.splinterBrowser import browserWaitTime

def requestsHandlingWhenTimeoutOccur(url, browserName):
    timeSleepEight()
    browser = buildSplinterBrowserHeadless(browserName)
    timeSleepRandomly()
    browser.visit(url)
        
# 正式===============================================================================
def getPageInARow(input, output, keywordUrlPair, objectiveFolder, objective):
    begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        searchword = input.get()
        print('getPageInARow is in new process %s, %s ' % (getPageInARow_proc, os.getpid()))
        print()
        eraseRawData(objectiveFolder, objective, searchword)
        mkdirForRawData(objectiveFolder, objective, searchword)

        url = keywordUrlPair[searchword]

        try:
            # 建立browser的代碼放進while True裡面，就可以避免「同一個瀏覽器」持續拜訪網頁時，被拒絕的情況。
            timeSleepTwo()
            browser = buildSplinterBrowserHeadless('chrome')
            timeSleepRandomly()
            browser.visit(url)
        except (ConnectionRefusedError, TimeoutException) as e:
            print(f"{thisPID}__{getPageInARow_proc}  讀取{searchword}第 1 頁有問題。", e)
            print(f"{thisPID}__{getPageInARow_proc}  重建browser物件，進行再處理!")
            timeSleepFour()
            browser = buildSplinterBrowserHeadless('chrome')
            timeSleepRandomly()
            browser.visit(url)
            print(f"再處理{searchword}第 1 頁>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功！")
        else:
            print(f"讀取{searchword}第 1 頁>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功！")

        browserWaitTime(browser)
        
        timeSleepTwo()
        
        tempHtml = browser.html

        timeSleepRandomly()

        soup = BeautifulSoup(tempHtml,'html.parser')
        
        totalPage = interDiv(searchNums(soup.select_one('.totalTxt').text),30)
        
        print('------接下來要處理 ' + searchword + ' 的頁數---------', totalPage, '頁')
        print()
        
        with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/1_{totalPage}_{searchword}.txt", 'w', encoding='utf-8')as f:
            f.write(str(soup))
        print()
        print(f'成功寫出  {searchword}  第 1 頁')

        i_browser = 1
        try:
            browser.quit()
            print(f"成功關閉 browser{getPageInARow_proc}++++++++++++++++++++++++++++++")
        except:
            print(f"放棄 {thisPID}__{getPageInARow_proc} 的 第{i_browser}個browser。")
            i_browser += 1
            print(f"kill {thisPID}__{getPageInARow_proc} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            os.kill(thisPID, signal.SIGKILL)
        
        # 休息久一點，讓所有searchword的第一頁都有被讀到。
        timeSleepEight()
        timeSleepEight()
        
        for num in range(2, totalPage+1):
            strNum = str(num)
            consecutiveData = searchword + "+" + strNum + "+" + str(totalPage) + "+" + re.sub(r"curPage=1",f"curPage={strNum}",url)
            output.put(consecutiveData)
            print(f'這裡是getPageInARow，準備送給  getPageInARowAdvanced  處理:  {searchword} 的 第 {strNum} 頁，總共{totalPage}')
            print()
        input.task_done()  #通知main process此次的input處理完成！
        end = timeCalculate()
        print(f'{thisPID}__getPageInARow 累計耗時：{end-begin} 秒')



# 補救用===============================================================================
# def getPageInARow(input, output, index, keywordUrlPair, dirName):
#     while True:
#         browser = buildSplinterBrowserHeadless('chrome')
#         print('getPageInARow is in new process %s, %s ' % (getPageInARow_proc, os.getpid()))
#         print()
        
#         keyword = input.get()
#         url = keywordUrlPair[keyword]
        
#         compensationList = [6, 25, 2, 11, 20, 21, 27, 33, 5, 28, 36]
#         for num in compensationList:
#             strNum = str(num)
#             consecutiveData = keyword + "+" + strNum + "+" + re.sub(r"curPage=1",f"curPage={strNum}",url)
#             output.put(consecutiveData)
#             print(f'這裡是getPageInARow，準備送給  getPageInARowAdvanced  處理:  {keyword} 的 第 {strNum} 頁，總共{len(compensationList)}')
#             print()
#         input.task_done()  #通知main process此次的input處理完成！
#         timeSleepTwo() #暫停幾秒來模擬現實狀況。

def getPageInARowAdvanced(input, objectiveFolder, objective):
    begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        consecutiveUrl = input.get()
        searchword, page, totalPage, url = consecutiveUrl.split('+')
        print(url)
        print(f"{thisPID}__{getPageInARowAdvanced_proc} 開始處理 {searchword} 的第 {page} 頁：")
        
        try:
            # 建立browser的代碼放進while True裡面，就可以避免「同一個瀏覽器」持續拜訪網頁時，被拒絕的情況。
            timeSleepFour()
            browser = buildSplinterBrowserHeadless('chrome')
            timeSleepRandomly()
            browser.visit(url)
        except (ConnectionRefusedError, TimeoutException) as e:
            #要是頁面在此出錯，那麼要怎麼繼續處理錯誤的頁面？
            print(f"{thisPID}__{getPageInARowAdvanced_proc} 讀取 {searchword} 第 {page} 頁有問題。",e)
            print(f"{thisPID}__{getPageInARowAdvanced_proc} 重建browser物件，進行再處理-----------------------------")
            # timeSleepFour()
            # browser = buildSplinterBrowserHeadless('chrome')
            # timeSleepRandomly()
            # browser.visit(url)
            try:
                requestsHandlingWhenTimeoutOccur(url, "chrome")
            except (ConnectionRefusedError, TimeoutException) as e:
                print(f"{searchword}第 {page} 頁進行第三次處理。。。")
                requestsHandlingWhenTimeoutOccur(url, "chrome")
                print(f"再處理{searchword}第 {page} 頁，成功！")
            else:
                print(f"再處理{searchword}第 {page} 頁，成功！")
        else:
            print(f"讀取{searchword}第 {page} 頁，成功！")

        
        browserWaitTime(browser)

        timeSleepTwo()

        tempHtml = browser.html

        timeSleepRandomly()
        
        soup = BeautifulSoup(tempHtml,'html.parser')

        with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/{page}_{totalPage}_{searchword}.txt", 'w', encoding='utf-8')as f:
            f.write(str(soup))
        print()
        print(f'{thisPID}  成功寫出  {searchword}  第{page}頁，總共{totalPage} 頁。')
    
        try:
            browser.quit()
            print(f"成功關閉 browser{thisPID}__{getPageInARowAdvanced_proc}++++++++++++++++++++++++++++++")
        except:
            print(f"放棄 {thisPID}__{getPageInARowAdvanced_proc} 這個browser。")
            print(f"kill {thisPID}__{getPageInARowAdvanced_proc} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            os.kill(thisPID, signal.SIGKILL)
        input.task_done()  #通知main process此次的input處理完成！
        end = timeCalculate()
        print(f'{thisPID}__getPageInARowAdvanced 累計耗時：{end-begin} 秒')

if __name__ == '__main__':
    
    objectiveFolder = "rawData"

    objective = "momo"

    begin = timeCalculate()
    
    print('start in main process %s' %os.getpid())

    print('-------------------------------------------------------------------------')
    

    # 共同佇列宣告
    searchword_queue = mp.JoinableQueue()
    url_queue = mp.JoinableQueue()
    

    # 啟動進程
    Process_1 = []
    for p in range(8):
        getPageInARow_proc = mp.Process(target=getPageInARow, args=(searchword_queue, url_queue, _momoKeywordUrlPair, objectiveFolder, objective,))
        getPageInARow_proc.daemon = True
        getPageInARow_proc.start()
        print(f'建立第{p}個 getPageInARow_proc, {getPageInARow_proc}')
        Process_1.append(getPageInARow_proc)
    
    Process_2 = []
    for u in range(30):
        getPageInARowAdvanced_proc = mp.Process(target=getPageInARowAdvanced, args=(url_queue,objectiveFolder, objective,))
        getPageInARowAdvanced_proc.daemon = True
        getPageInARowAdvanced_proc.start()
        print(f'建立第{u}個 getPageInARowAdvanced_proc, {getPageInARowAdvanced_proc}')
        Process_2.append(getPageInARowAdvanced_proc)


    # 主行程
    distributeKeyword(_momoKeywordUrlPair, searchword_queue)
    print("=============main process distributeKeyword 已經完成任務了。=============")
    
    #通知main process 完成事情。
    searchword_queue.join()
    url_queue.join()


    print('Multiprocessing has done all jobs!')
    
    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')
    
    for proc in Process_2:
        proc.terminate()
        print(f'{proc} has terminated!')

    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))
