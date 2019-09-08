# -*- coding:utf-8 -*-
"""
程式名稱：
程式描述：

    1. 

    2. 

備　　註：

#
家電促銷
家電節能補助
家電汰舊換新


完成！一共耗時：1575.4612159729004 秒

output's data structure: 
{
    dateTime: ....,
    keyword: ...,
    newsTotalNum: ..., 
    newsUrl:{
        url: [newsTitle, publisher, date],
        url: 
    }
}



"""

from bs4 import BeautifulSoup
from splinter.exceptions import ElementDoesNotExist
import multiprocessing as mp

import random
import sys
import os
import requests
import json
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 專案資料夾下第二層，用兩個path.dirname
sys.path.append(_BASE_PATH)

from libs.httpRequests import _headers
from libs.regex import discardSpace
from libs.timeWidget import timeSleepRandomly
from libs.timeWidget import timeCalculate
from libs.timeWidget import timeSleepOne
from libs.timeWidget import timeStampGenerator
from libs.timeWidget import timeStampCalculate
from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData

from libs.multiProcessing import distributeKeyword
from libs.multiProcessing import _googleSearchWord
from libs.splinterBrowser import buildSplinterBrowser
from libs.splinterBrowser import buildSplinterBrowserHeadless
from libs.splinterBrowser import browserWaitTime


def searchwordKeyInAndEnter(browser, searchword):
    # 輸入匡輸入
    # //*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input
    # //*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input # 可以work
    
    try:
        browser.find_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').fill(searchword)
        timeSleepOne()
    except AttributeError as e:
        browser.find_by_xpath('//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input').fill(searchword)
        timeSleepOne()
    # enter
    browser.find_by_xpath('//*[@id="tsf"]/div[2]/div/div[2]/div[2]/div/center/input[1]').click()
    timeSleepRandomly()

def findOutNws(browser, topTabList):
    findOutNws = {}
    findOutNws['1'] = "全部"
    for n in topTabList:
        broTmp = browser.find_by_xpath(f'//*[@id="hdtb-msb-vis"]/div[{n}]/a')
        if broTmp.text == "新聞":
            print(f"第 {n} 是新聞")
        findOutNws[str(n)] = broTmp.text
        timeSleepOne()
    return findOutNws

def humanSimulate(browser, topTabList):
    randomNum = random.choice(topTabList)
    print("對 topTabList 第",randomNum,"項，做擬人================")
    try:
        browser.find_by_xpath(f'//*[@id="hdtb-msb-vis"]/div[{randomNum}]/a').mouse_over()
        timeSleepRandomly()
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        timeSleepOne()
        browser.execute_script('window.scrollTo(0,0);')

        if browser.is_element_present_by_xpath('//*[@id="logo"]/img'):
            browser.find_by_xpath('//*[@id="logo"]/img').mouse_over()
        elif browser.is_element_present_by_xpath('//*[@id="logocont"]/a/img'):
            browser.find_by_xpath('//*[@id="logocont"]/a/img').mouse_over()
    except AttributeError as e: # 找不到element 來mouse_over() ； //*[@id="logocont"]/a/img      //*[@id="logo"]/img    左上r角的google有兩種logo位置
        print("擬人化操作找不到 Element。", e)
        pass
    

def elementUrlExtract(browser, firstPage, topTabList, elementUrl, newsDictInner, searchword):
    try:
        for order in elementUrl:
            broUrl = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/h3/a')
            broPublisher = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/div[1]/span[1]')
            broDate = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/div[1]/span[3]')
            newsUrl = broUrl["href"]
            newsTitle = broUrl.text
            publisher = broPublisher.text
            date = broDate.text

            print(f"擷取 『{searchword}』  第 {firstPage} 頁 ， 第 {order} 項================")
            print(newsUrl)
            print(newsTitle)
            print(publisher)
            print(date)
            
            timeSleepRandomly()
            newsDictInner[newsUrl] = [newsTitle, discardSpace(publisher), timeStampCalculate(date)]

            humanSimulate(browser, topTabList)
            
    except ElementDoesNotExist as e: # 新聞標的不到10項時。
        print(f"{searchword} 新聞標的不到10項，準備關閉瀏覽器。", e)
        print(f"成功擷取 『{searchword}』  當前頁的新聞連結。")
        pass
    else:
        print(f"成功擷取 『{searchword}』  當前頁的新聞連結。")

def judgeNextPage(browser, searchword):
    try:
        browser.find_by_xpath('//*[@id="pnnext"]').click()
        return 1
    except AttributeError as e: # 沒有下一頁了！
        print(f"『{searchword}』 沒有下一頁了，準備關閉瀏覽器。", e)
        pass


def getPageInARow(input, url, firstPage, topTabList, elementUrl, objectiveFolder, objective, *args):
    begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        searchword = input.get()

        mkdirForRawData(objectiveFolder, objective, "google", keyword=searchword)
        browser = buildSplinterBrowserHeadless("chrome")
        
        browser.visit(url)
        browserWaitTime(browser)

        searchwordKeyInAndEnter(browser, searchword)
        browser.driver.set_window_size(1024,768)

        forSureNws = findOutNws(browser, topTabList)
        keyNews = [key for key in forSureNws if forSureNws[key] == '新聞'].pop()
        # 擬人化mouse_over要排除新聞tab
        topTabList.remove(int(keyNews))

        print(f"點擊 topTabList {keyNews} 去到 新聞頁")
        #點擊新聞tab
        browser.find_by_xpath(f'//*[@id="hdtb-msb-vis"]/div[{keyNews}]/a').click()
        timeSleepRandomly()

        newsDict = {}
        newsDictInner = {}
        while True:
            print(f"進行 {searchword} 第", firstPage, "頁")
            elementUrlExtract(browser, firstPage, topTabList, elementUrl, newsDictInner, searchword)
            judgment = judgeNextPage(browser, searchword)
            if judgment:
                print(f"『{searchword}』 仍有下一頁，繼續爬取！")
                firstPage += 1
                pass
            else:
                browser.quit()
                break
        
        timeStamp =  timeStampGenerator()
        newsTotalNum = len(newsDictInner)
        newsDict["dateTime"] = timeStamp
        newsDict["keyword"] = searchword
        newsDict["newsTotalNum"] = newsTotalNum
        newsDict["newsUrl"] = newsDictInner

        with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/google/{searchword}/google_{timeStamp}_{newsTotalNum}_{searchword}.json", 'w', encoding='utf-8')as f:
            json.dump(newsDict, f, indent=2, ensure_ascii=False)
        print(f'{thisPID}  成功寫出  google_{timeStamp}_{newsTotalNum}_{searchword}.json ')

        input.task_done()
        end = timeCalculate()
        print(f'{thisPID}_getPageInARaw 累計耗時：{end-begin} 秒')

if __name__ == '__main__':

    objectiveFolder = "rawData"
    objective = "news"

    topTabList = [row for row in range(2,6)] #新聞、圖片、地圖、影片；[更多]__>xpath不同，無法準確mouse_over()
    elementUrl = [row for row in range(1,11)] #一頁有10個標的

    url = "https://www.google.com/"
    firstPage = 1

    begin = timeCalculate()

    #共同佇列
    keyword_queue = mp.JoinableQueue()

    #啟動進程
    Process_1 = []
    for p in range(3):
        getPageInARow_proc = mp.Process(target=getPageInARow, args=(keyword_queue, url, firstPage, topTabList, elementUrl, objectiveFolder, objective,))
        getPageInARow_proc.daemon = True
        getPageInARow_proc.start()
        print(f'建立第{p}個 getPageInARow_proc, {getPageInARow_proc}')
        Process_1.append(getPageInARow_proc)

    #主進程
    distributeKeyword(_googleSearchWord, keyword_queue)
    print("=============main process distributeKeyword 已經完成任務了。=============")

    #通知main process 完成事情。 寫超過兩個queue，程式將無法正常終止。
    keyword_queue.join()
    print('Multiprocessing has done all jobs!')
    
    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')

    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))