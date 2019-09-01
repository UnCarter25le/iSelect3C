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


7317 ===========================================
Process Process-7:
Traceback (most recent call last):
  File "/home/bluevc/.pyenv/versions/3.6.8/lib/python3.6/multiprocessing/process.py", line 258, in _bootstrap
    self.run()
  File "/home/bluevc/.pyenv/versions/3.6.8/lib/python3.6/multiprocessing/process.py", line 93, in run
    self._target(*self._args, **self._kwargs)
  File "/home/bluevc/2019/iSelect3C/crawler/momoMulti.py", line 171, in getPageInARowAdvanced
    browser = buildSplinterBrowserHeadless('chrome')
  File "/home/bluevc/2019/iSelect3C/libs/splinterBrowser.py", line 46, in buildSplinterBrowserHeadless
    browser = Browser(driver_name = browserName, headless=True, incognito=True)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/splinter/browser.py", line 64, in Browser
    return driver(*args, **kwargs)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/splinter/driver/webdriver/chrome.py", line 43, in __init__
    self.driver = Chrome(options=options, **kwargs)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/selenium/webdriver/chrome/webdriver.py", line 81, in __init__
    desired_capabilities=desired_capabilities)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 157, in __init__
    self.start_session(capabilities, browser_profile)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 252, in start_session
    response = self.execute(Command.NEW_SESSION, parameters)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/selenium/webdriver/remote/errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally
  (Driver info: chromedriver=2.36.540471 (9c759b81a907e70363c6312294d30b6ccccc2752),platform=Linux 4.15.0-55-generic x86_64)






30個process
完成！一共耗時：925.360677242279 秒
完成！一共耗時：1003.4922308921814 秒

14個
成！一共耗時：1825.5846257209778 秒
try except 要改善  已有改善，待嘗試。
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
from selenium.common.exceptions import (
                                        TimeoutException,
                                        WebDriverException
                                    )


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)

from libs.manipulateDir import (
                              mkdirForRawData,
                              eraseRawData
                              )
from libs.timeWidget import (
                            timeSleepRandomly,
                            timeSleepEight,
                            timeSleepOne,
                            timeSleepTwo,
                            timeSleepFour,
                            timeCalculate
                            )
from libs.multiProcessing import (
                              distributeKeyword,
                              _momoKeywordUrlPair
                              )
from libs.manipulateDir import initialFileZeroUnderscoreInt
from libs.regex import (
                      searchNums,
                      interDiv
                      )
from libs.splinterBrowser import (
                              buildSplinterBrowserHeadless,
                              browserWaitTime
                                )

def requestsHandlingWhenTimeoutOccur(url, browserName):
    timeSleepEight()
    browser = buildSplinterBrowserHeadless(browserName)
    timeSleepRandomly()
    browser.visit(url)
        
# 正式===============================================================================
def getPageInARow(input, output, keywordUrlPair, objectiveFolder, objective):
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        searchword = input.get()
        print('getPageInARow is in new process %s, %s ' % (getPageInARow_proc, thisPID))
        print()
        eraseRawData(objectiveFolder, objective, searchword)
        mkdirForRawData(objectiveFolder, objective, searchword)

        url = keywordUrlPair[searchword]

        # 建立browser的代碼放進while True裡面，就可以避免「同一個瀏覽器」持續拜訪網頁時，被拒絕的情況。
        for i in range(3):
            try:
                timeSleepOne()
                timeSleepRandomly()

                browser = buildSplinterBrowserHeadless('chrome')
                
                timeSleepRandomly()
                
                browser.visit(url)
                
                browserWaitTime(browser)
                timeSleepTwo()
                
                tempHtml = browser.html
                
                timeSleepRandomly()
                soup = BeautifulSoup(tempHtml,'html.parser')
                print(f"讀取{searchword}第 1 頁>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功！")
                break
            except (ConnectionRefusedError, TimeoutException, WebDriverException) as e:
                print(f"{thisPID}__{getPageInARow_proc}  讀取{searchword}第 1 頁有問題。", e)
                print(f"{thisPID}__{getPageInARow_proc}  重建browser物件，進行再處理 {i} 次!")
                timeSleepFour()
                timeSleepRandomly()
                soup = ""
            # else:
            #     print(f"讀取{searchword}第 1 頁>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>成功！")

        try:
            totalPage = interDiv(searchNums(soup.select_one('.totalTxt').text),30)
        except AttributeError as e:
            print("getPageInARow 出錯", e)
            # 讓程式強制停下來
            raise
        
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
            # print(f'這裡是getPageInARow，準備送給  getPageInARowAdvanced  處理:  {searchword} 的 第 {strNum} 頁，總共{totalPage}')
            print()
        input.task_done()  #通知main process此次的input處理完成！
        end = timeCalculate()
        print(f'{thisPID}__getPageInARow 累計耗時：{end-begin} 秒')



def getPageInARowAdvanced(input, objectiveFolder, objective):
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        consecutiveUrl = input.get()
        searchword, page, totalPage, url = consecutiveUrl.split('+')
        # print(url)
        print(f"{thisPID}__{getPageInARowAdvanced_proc} 開始處理 {searchword} 的第 {page} 頁：")
        
        # 建立browser的代碼放進while True裡面，就可以避免「同一個瀏覽器」持續拜訪網頁時，被拒絕的情況。
        for i in range(3):
            try:
                timeSleepFour()
                
                browser = buildSplinterBrowserHeadless('chrome')
                
                timeSleepRandomly()
                
                browser.visit(url)
                
                browserWaitTime(browser)
                timeSleepTwo()
                
                tempHtml = browser.html
                timeSleepRandomly()
                
                soup = BeautifulSoup(tempHtml,'html.parser')
                print(f"讀取{searchword}第 {page} 頁，成功！")
                break
            except (ConnectionRefusedError, TimeoutException, WebDriverException) as e:
                print(f"{thisPID}__{getPageInARowAdvanced_proc} 讀取 {searchword} 第 {page} 頁有問題。",e)
                print(f"{thisPID}__{getPageInARowAdvanced_proc} 重建browser物件，進行再處理 {i} 次!")
                timeSleepFour()
                timeSleepRandomly()
                soup = ""
            # else:
            #     print(f"讀取{searchword}第 {page} 頁，成功！")


        if not soup:
            badRequestRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/badRequest"
            with open(f"{badRequestRoute}/badRequest_{searchword}.txt", "a",  newline='', encoding='utf-8')as f: # newline沒作用...
                errorMessage = url + "\n"
                f.write(errorMessage)   #writelines作用在errorMessage是list時
        
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

    eraseRawData(objectiveFolder, objective, "badRequest")
    mkdirForRawData(objectiveFolder, objective, "badRequest")
    print('-------------------------------------------------------------------------')
    

    # 共同佇列宣告
    searchword_queue = mp.JoinableQueue()
    url_queue = mp.JoinableQueue()
    

    # 啟動進程
    Process_1 = []
    for p in range(4):
        getPageInARow_proc = mp.Process(target=getPageInARow, args=(searchword_queue, url_queue, _momoKeywordUrlPair, objectiveFolder, objective,))
        getPageInARow_proc.daemon = True
        getPageInARow_proc.start()
        print(f'建立第{p}個 getPageInARow_proc, {getPageInARow_proc}')
        Process_1.append(getPageInARow_proc)
    
    Process_2 = []
    for u in range(10):
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
