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

"""

from bs4 import BeautifulSoup
import requests
import json
import re
import csv
import os
# import shutil #high level os
import sys
import time
# import random
import signal
# from math import ceil
import multiprocessing as mp


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)

# from urllib3.connectionpool import MaxRetryError
from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.time import timeSleepRandomly
from libs.time import timeSleepOne
from libs.time import timeSleepTwo
from libs.time import timeSleepFour
from libs.multiProcessing import distributeKeyword
from libs.manipulateDir import initialFile
from libs.regex import searchNums
from libs.regex import interDiv
from libs.splinterBrowser import buildSplinterBrowser
from libs.splinterBrowser import browserWaitTime

        
# 正式===============================================================================
def getPageInARow(input, output, keywordUrlPair, objectiveFolder, objective):
    begin = time.time()
    thisPID = os.getpid()
    browser = buildSplinterBrowser('chrome')
    while True:
        print(thisPID,"===========================================")
        searchword = input.get()

        print('getPageInARow is in new process %s, %s ' % (getPageInARow_proc, os.getpid()))
        print()
        eraseRawData(objectiveFolder, objective, searchword)
        mkdirForRawData(objectiveFolder, objective, searchword)

        url = keywordUrlPair[searchword]
          
        try:
            browser.visit(url)
        except:    
            print(f"{thisPID}__{getPageInARow_proc}  讀取{searchword}第 1 頁有問題。")
                    
        browserWaitTime(browser)
        
        timeSleepTwo()
        
        tempHtml = browser.html

        
        
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
            print(f"放棄{getPageInARow_proc} 的 第{i_browser}個browser。")
            i_browser += 1
        
        timeSleepRandomly()
        
        for num in range(2, totalPage+1):
            strNum = str(num)
            consecutiveData = searchword + "+" + strNum + "+" + str(totalPage) + "+" + re.sub(r"curPage=1",f"curPage={strNum}",url)
            output.put(consecutiveData)
            print(f'這裡是getPageInARow，準備送給  getPageInARowAdvanced  處理:  {searchword} 的 第 {strNum} 頁，總共{totalPage}')
            print()
        input.task_done()  #通知main process此次的input處理完成！
        print(f"準備kill {thisPID}__{getPageInARow_proc} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        end = time.time()
        print(f'{thisPID}__getPageInARow 累計耗時：{0} 秒'.format(end-begin))
        print(f"kill {thisPID}__{getPageInARow_proc} <<<<<<<<<<<<<<")
        os.kill(thisPID, signal.SIGKILL)



# 補救用===============================================================================
# def getPageInARow(input, output, index, keywordUrlPair, dirName):
#     browser = buildSplinterBrowser('chrome')
#     while True:
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
#         time.sleep(2) #暫停幾秒來模擬現實狀況。

def getPageInARowAdvanced(input, objectiveFolder, objective):
    begin = time.time()
    thisPID = os.getpid()
    browser = buildSplinterBrowser('chrome')
    while True:
        consecutiveUrl = input.get()

        searchword, page, totalPage, url = consecutiveUrl.split('+')

        print(url)
        
        print(f"{thisPID}__{getPageInARowAdvanced_proc} 開始處理 {searchword} 的第 {page} 頁：")
        
        timeSleepRandomly()
        
        try:
            browser.visit(url)
        except:    
            print(f"{thisPID}__{getPageInARowAdvanced_proc} 讀取 {searchword} 第 {page} 頁有問題。")
#             try:
#                 browser.quit()
#                 print(f"成功關閉 browser")
#             except:
#                 print(f"放棄")
#             for row in range(2):
#                 try:
#                     timeSleepRandomly()
#                     browser.visit(url)
#                 except:
#                     print(f"{thisPID}__{getPageInARowAdvanced_proc}  讀取{keyword}第 {page} 頁有問題。")
#                 else:
#                     break
        browserWaitTime(browser)
        
        timeSleepTwo()

        tempHtml = browser.html

        timeSleepRandomly()
        
        soup = BeautifulSoup(tempHtml,'html.parser')

        with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/{page}_{totalPage}_{searchword}.txt", 'w', encoding='utf-8')as f:
            f.write(str(soup))
        print()
        print(f'{thisPID}  成功寫出  {searchword}  第{page}頁')
    
        try:
            browser.quit()
            print(f"成功關閉 browser{thisPID}__{getPageInARowAdvanced_proc}++++++++++++++++++++++++++++++")
        except:
            print(f"放棄{thisPID}__{getPageInARowAdvanced_proc} 這個browser。")
        
        input.task_done()  #通知main process此次的input處理完成！
        print(f"準備kill {thisPID}__{getPageInARowAdvanced_proc} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        end = time.time()
        print(f'{thisPID}__getPageInARowAdvanced 累計耗時：{0} 秒'.format(end-begin))
        print(f"kill {thisPID}__{getPageInARowAdvanced_proc} <<<<<<<<<<<<<<")
        os.kill(thisPID, signal.SIGKILL)
        
# def dataMunging(input, index, keywordUrlPair, dirName):
#     begin = time.time()
#     domainUrl = "https://www.momoshop.com.tw"
#     while True:
#         dirNameAccept = input.get() #./14_電冰箱_20190505_MOMO/
#         for w in keywordUrlPair:
#             if w in dirNameAccept:
#                 keyword = w
#         print('dataMunging is in new process %s, %s ' % (dataMunging_proc, os.getpid()))
#         print()
#         print('------接下來要處理資料夾路徑「 ' + dirNameAccept + '」---------')
#         print()
        
#         infoDict = {}
#         productArray= [] 
#         innerDict = {}
        
#         for file in initialFile(dirNameAccept):
#             print('start' + file + '!')
            
#             with open(dirNameAccept + file)as f:
#                 inn = f.read() 
#             textSoup = BeautifulSoup(inn,'html.parser')
            
#             #總頁數
#             totalPage = interDiv(searchNums(textSoup.select_one('.totalTxt').text),30)
            
#             #一頁至多有30項
#             products = textSoup.select_one('.listArea').select_one('ul').select('li')
            
#             for item in products:
#                 innerDict = {}
#                 innerDict['id'] = item.attrs.get('gcode')
#                 innerDict['name'] = item.select_one('.goodsUrl').select_one('.prdName').text
#                 innerDict['originprice'] = item.select_one('.goodsUrl').select_one('.money .price').text.replace('$','').replace(',','')
#                 innerDict['pics'] = item.select_one('.goodsUrl img').attrs.get('src') 
#                 innerDict['detailUrl'] = domainUrl + item.select_one('.goodsUrl').attrs.get('href')
#                 productArray.append(innerDict)
                
#             infoDict['product'] = productArray
#             infoDict['keyword'] = keyword
            
            
#         keywordHasNums = len(infoDict['product'])
        
#         with open(f"./{index}_{keywordHasNums}_{keyword + dirName}.json","w",encoding="utf-8")as f:
#             json.dump(infoDict, f, indent=2, ensure_ascii=False)
        
#         print('這裡是 dataMunging ，處理完成: ' + dirNameAccept)
#         print()
#         end = time.time()
#         print('dataMunging 累計耗時：{0} 秒'.format(end-begin))
#         input.task_done()
#         time.sleep(2) #暫停幾秒來模擬現實狀況。

if __name__ == '__main__':
    
    keywordUrlPair = {"冰溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                 "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
                                 "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                    "冰溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                             "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
                             "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType")}
    # keywordUrlPair = {"冷暖空調":("https://www.momoshop.com.tw/search/searchShop.jsp"
    #                           "?keyword=%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF"
    #                           "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
    #                   "除濕機":("https://www.momoshop.com.tw/search/searchShop.jsp"
    #                          "?keyword=%E9%99%A4%E6%BF%95%E6%A9%9F"
    #                          "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
    #                   "電冰箱":("https://www.momoshop.com.tw/search/searchShop.jsp"
    #                          "?keyword=%E9%9B%BB%E5%86%B0%E7%AE%B1"
    #                          "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
    #                   "電熱水瓶":("https://www.momoshop.com.tw/search/searchShop.jsp"
    #                           "?keyword=%E9%9B%BB%E7%86%B1%E6%B0%B4%E7%93%B6"
    #                           "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
    #                   "溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
    #                             "?keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
    #                             "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
    #                   "溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp?"
    #                             "keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
    #                             "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
    #                   "冰溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
    #                              "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
    #                              "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
    #                   "冰溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp"
    #                              "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
    #                              "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType")}
    
    objectiveFolder = "rawData"

    objective = "momo"

    begin = time.time()
    
    print('start in main process %s' %os.getpid())

    print('-------------------------------------------------------------------------')
    

    # 共同佇列宣告
    searchword_queue = mp.JoinableQueue()
    url_queue = mp.JoinableQueue()
    

    # 啟動進程
    Process_1 = []
    for p in range(2):
        getPageInARow_proc = mp.Process(target=getPageInARow, args=(searchword_queue, url_queue, keywordUrlPair, objectiveFolder, objective,))
        getPageInARow_proc.daemon = True
        getPageInARow_proc.start()
        print(f'建立第{p}個 getPageInARow_proc, {getPageInARow_proc}')
        Process_1.append(getPageInARow_proc)
    
    Process_2 = []
    for u in range(20):
        getPageInARowAdvanced_proc = mp.Process(target=getPageInARowAdvanced, args=(url_queue,objectiveFolder, objective,))
        getPageInARowAdvanced_proc.daemon = True
        getPageInARowAdvanced_proc.start()
        print(f'建立第{u}個 getPageInARowAdvanced_proc, {getPageInARowAdvanced_proc}')
        Process_2.append(getPageInARowAdvanced_proc)


    # 主行程
    distributeKeyword(keywordUrlPair, searchword_queue)
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

    end = time.time()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))
