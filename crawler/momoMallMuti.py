# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json
import re
# import csv
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
                                        WebDriverException,
                                        StaleElementReferenceException
                                    )
                                
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.manipulateDir import (
                              mkdirForRawData,
                              eraseRawData,
                              folderDataManipulate,
                              initialFileZeroUnderscoreInt
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
                              multiProcessToolBox
                              )

from libs.regex import (
                      numsHandler
                      )
from libs.splinterBrowser import (
                              buildSplinterBrowserHeadless,
                              browserWaitTime,
                              browserQuit,
                              browserSetWindowSize
                                )
from libs.httpRequests import (
                            keywordResourcePair,
                            momoMallRequests
                              )     



def getPageInARow(input, output, folderWorker, momoMallBrowser):
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        searchword = input.get()
        print('getPageInARow is in new process %s, %s ' % (getPageInARow_proc, thisPID))
        folderWorker.eraseRawData(searchword)
        folderWorker.mkdirForRawData(searchword)
        
        
        url = momoMallBrowser.keywordResourcePair._momoMallKeywordUrlPair[searchword]
        

        # 建立browser的代碼放進while True裡面，就可以避免「同一個瀏覽器」持續拜訪網頁時，被拒絕的情況。
        for i in range(4):
            try:
                timeSleepOne()
                timeSleepRandomly()
                
                browser = momoMallBrowser.intersectionForCrawl(folderWorker.objective)
                
                timeSleepRandomly()
                
                browser.visit(url)
                
                browserWaitTime(browser)
                timeSleepTwo()
                
                #點擊「準確度」，頁數跳至第1頁
                try:
                    buyingTendency = momoMallBrowser.browserClickSearchType(browser, 1)
                    browserWaitTime(browser)
                    timeSleepTwo()
                except AttributeError as e:
                    print(f"{thisPID}__{getPageInARow_proc}  {searchword} 第1頁 點擊準確度有問題。", e)
                    print(f"{thisPID}__{getPageInARow_proc}  重建browser物件，進行再處理 {i} 次!")
                    browserQuit(browser, thisPID, getPageInARow_proc)
                    timeSleepFour()
                    soup = ""
                    continue
                    
                

                tempHtml = browser.html
                
                timeSleepRandomly()
                soup = BeautifulSoup(tempHtml, 'lxml')
                print(f"-----------------讀取{searchword}_{buyingTendency}第 1 頁-----------------成功！")

                try:
                    ## current page and total page '頁數5/286'

                    pageState = browser.find_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/dl/dt/span')
                    totalPage = int(pageState.text.split('/')[1])
                    currentPage = int(numsHandler.searchFloatNums(pageState.text.split('/')[0]))
                    print(f"-----------------讀取{searchword}_{buyingTendency} 總頁數-----------------成功！")
                except AttributeError as e:
                    print(f"getPageInARow __{searchword}__出錯", e, "重抓一次！")
                    # 讓程式強制停下來 # 觀察下來，「raise」只會讓當前執行的process停下來，並不會讓「整體」process停下來。
                    # 因此不適合用「raise」。
                    # raise
                    currentPage = 1 # 自訂
                    totalPage = 3 # 自訂
                    continue
                break
            except (ConnectionRefusedError, TimeoutException, WebDriverException) as e:
                print(f"{thisPID}__{getPageInARow_proc}  讀取{searchword}第 1 頁有問題。", e)
                print(f"{thisPID}__{getPageInARow_proc}  重建browser物件，進行再處理 {i} 次!")
                browserQuit(browser, thisPID, getPageInARow_proc)
                timeSleepFour()
                timeSleepRandomly()
                soup = ""
            except StaleElementReferenceException as e:
                print("----------------StaleElementReferenceException----------------")
                print(f"{thisPID}__{getPageInARow_proc}  讀取{searchword}第 1 頁有問題。", e)
                print(f"{thisPID}__{getPageInARow_proc}  重建browser物件，進行再處理 {i} 次!")
                browserQuit(browser, thisPID, getPageInARow_proc)
                timeSleepFour()
                timeSleepRandomly()
                soup = ""
								
        if not soup:
            errorMessage = f"{url}__{currentPage}__" + "\n"
            folderWorker.writeOutFile(f"{folderWorker._BASE_PATH}/dataMunging/{folderWorker.objectiveFolder}/{folderWorker.objective}/badRequest", 
                                  f"badRequest_{searchword}.txt", 
                                  errorMessage, 
                                  writeOutType="a")
        
        folderWorker.writeOutFile(f"{folderWorker._BASE_PATH}/dataMunging/{folderWorker.objectiveFolder}/{folderWorker.objective}/{searchword}", 
                                  f"1_{totalPage}_{searchword}.txt", soup)         
            
        print(f'成功寫出  {searchword}  第 {currentPage} 頁')
        
        print('------接下來要處理 ' + searchword + ' 的頁數---------', totalPage, '頁')
        

        browserQuit(browser, thisPID, getPageInARow_proc)

        
        # 休息久一點，讓所有searchword的第一頁都有被讀到。
        timeSleepEight()
        timeSleepEight()
        timeSleepEight()

        for num in range(2, totalPage+1):
            strNum = str(num)
            consecutiveData = searchword + "+" + strNum + "+" + str(totalPage)
            output.put(consecutiveData)
            # print(f'這裡是getPageInARow，準備送給  getPageInARowAdvanced  處理:  {searchword} 的 第 {strNum} 頁，總共{totalPage}')
            # print()
        
        input.task_done()  #通知main process此次的input處理完成！
        end = timeCalculate()
        print(f'{thisPID}__getPageInARow 累計耗時：{end-begin} 秒')



def getPageInARowAdvanced(input, folderWorker, momoMallBrowser):
    """
    開始對POST網址進行splinter的點擊
    """
    thisPID = os.getpid()
    while True:
        # print(thisPID,"===========================================")
        consecutiveData = input.get()
        searchword, currentPage, totalPage = consecutiveData.split('+')
        
        url = momoMallBrowser.keywordResourcePair._momoMallKeywordUrlPair[searchword]

        # 建立browser的代碼放進while True裡面，就可以避免「同一個瀏覽器」持續拜訪網頁時，被拒絕的情況。
        for i in range(4):
            try:
                timeSleepFour()
                
                browser = momoMallBrowser.intersectionForCrawl(folderWorker.objective)
                
                timeSleepRandomly()
                
                browserSetWindowSize(browser, horizon=1920, vertical=1080)
                timeSleepOne()

                browser.visit(url)
                
                browserWaitTime(browser)
                timeSleepTwo()
                
                #點擊「準確度」，頁數跳至第1頁
                try:
                    buyingTendency = momoMallBrowser.browserClickSearchType(browser, 1)
                    browserWaitTime(browser)
                    timeSleepTwo()
                except AttributeError as e:
                    print(f"{thisPID}__{getPageInARowAdvanced_proc}  {searchword} 在第{currentPage}頁點擊準確度有問題。", e)
                    print(f"{thisPID}__{getPageInARowAdvanced_proc}  重建browser物件，進行再處理 {i} 次!")
                    browserQuit(browser, thisPID, getPageInARowAdvanced_proc)
                    timeSleepFour()
                    soup = ""
                    continue
                
                # 點擊至正確的頁數
                momoMallBrowser.browserClickPageNumber(browser, currentPage, totalPage, searchword)
                
                tempHtml = browser.html
                timeSleepRandomly()

                #擬人
                momoMallBrowser.humanSimulate(browser)
                
                soup = BeautifulSoup(tempHtml,'lxml')
                # print(f"讀取{searchword}第 {currentPage} 頁，成功！")
                break
            except (ConnectionRefusedError, TimeoutException, WebDriverException) as e:
                print(f"{thisPID}__{getPageInARowAdvanced_proc} 讀取 {searchword} 第 {currentPage} 頁有問題。",e)
                print(f"{thisPID}__{getPageInARowAdvanced_proc} 重建browser物件，進行再處理 {i} 次!")
                browserQuit(browser, thisPID, getPageInARowAdvanced_proc)
                timeSleepFour()
                timeSleepRandomly()
                soup = ""
            # else:
            #     print(f"讀取{searchword}第 {page} 頁，成功！")


        if not soup:
            errorMessage = f"{url}__{currentPage}__" + "\n"
            folderWorker.writeOutFile(f"{folderWorker._BASE_PATH}/dataMunging/{folderWorker.objectiveFolder}/{folderWorker.objective}/badRequest", 
                                  f"badRequest_{searchword}.txt", 
                                  errorMessage, 
                                  writeOutType="a")
        
        folderWorker.writeOutFile(f"{folderWorker._BASE_PATH}/dataMunging/{folderWorker.objectiveFolder}/{folderWorker.objective}/{searchword}", 
                                  f"{currentPage}_{totalPage}_{searchword}.txt", soup)         
            
        
        # print(f'{thisPID}  成功寫出  {searchword}  第{currentPage}頁，總共{totalPage} 頁。')
        
        
        browserQuit(browser, thisPID, getPageInARowAdvanced_proc)
        
        input.task_done()  #通知main process此次的input處理完成！
        end = timeCalculate()
        # print(f'{thisPID}__getPageInARowAdvanced 累計耗時：{end-begin} 秒')    
        


if __name__ == '__main__':

    objectiveFolder = "rawData"
    objective = "momoMall"
    folderWorker = folderDataManipulate(objectiveFolder=objectiveFolder, objective=objective)
    krPair = keywordResourcePair()
    momoMallBrowser = momoMallRequests(keywordResourcePair=krPair)
    
    begin = timeCalculate()
    
    print('start in main process %s' %os.getpid())

    folderWorker.eraseRawData("badRequest")
    folderWorker.mkdirForRawData("badRequest")
    print('-------------------------------------------------------------------------')
    

    # 共同佇列宣告
    searchword_queue = mp.JoinableQueue()
    page_queue = mp.JoinableQueue()

    # 啟動進程
    Process_1 = []
    for p in range(2):
        getPageInARow_proc = mp.Process(target=getPageInARow, args=(searchword_queue, page_queue, folderWorker, momoMallBrowser,))
        getPageInARow_proc.daemon = True
        getPageInARow_proc.start()
        print(f'建立第{p}個 getPageInARow_proc, {getPageInARow_proc}')
        Process_1.append(getPageInARow_proc)

    Process_2 = []
    for m in range(25):
        getPageInARowAdvanced_proc = mp.Process(target=getPageInARowAdvanced, args=(page_queue, folderWorker, momoMallBrowser,))
        getPageInARowAdvanced_proc.daemon = True
        getPageInARowAdvanced_proc.start()
        print(f'建立第{m}個 getPageInARowAdvanced_proc, {getPageInARowAdvanced_proc}')
        Process_2.append(getPageInARowAdvanced_proc)

    # 主行程
    multiProcessToolBox.distributeKeyword(momoMallBrowser.keywordResourcePair._momoMallKeywordUrlPair, searchword_queue)
    
    #通知main process 完成事情。
    searchword_queue.join()
    page_queue.join()

    print('Multiprocessing has done all jobs!')


    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')
    
    for proc in Process_2:
        proc.terminate()
        print(f'{proc} has terminated!')

    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))




    