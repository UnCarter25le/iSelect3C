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


完成！一共耗時：561.1129727363586 秒
改進後...
完成！一共耗時：2022.6550385951996 秒


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
from libs.multiProcessing import _weatherRecordAvailable
from libs.multiProcessing import distributeKeyword
from libs.splinterBrowser import buildSplinterBrowser
from libs.splinterBrowser import browserWaitTime


def searchwordKeyInAndEnter(browser, searchword):
    # 輸入匡輸入
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
    print(randomNum,"================")
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
    except AttributeError as e: # 找不到element 來mouse_over() ； //*[@id="logocont"]/a/img      //*[@id="logo"]/img    左上叫的google有兩種logo位置
        print("擬人化操作找不到 Element。", e)
        pass
    

def elementUrlExtract(browser, topTabList, elementUrl, newsDictInner):
    try:
        for order in elementUrl:
            broUrl = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/h3/a')
            broPublisher = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/div[1]/span[1]')
            broDate = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/div[1]/span[3]')
            newsUrl = broUrl["href"]
            newsTitle = broUrl.text
            publisher = broPublisher.text
            date = broDate.text

            print(newsUrl)
            print(newsTitle)
            print(publisher)
            print(date)
            
            timeSleepRandomly()
            newsDictInner[newsUrl] = [newsTitle, discardSpace(publisher), timeStampCalculate(date)]

            humanSimulate(browser, topTabList)
            
    except ElementDoesNotExist as e: # 新聞標的不到10項時。
        print("新聞標的不到10項，準備關閉瀏覽器。", e)
        print("成功擷取當前頁的新聞連結。")
        pass
    else:
        print("成功擷取當前頁的新聞連結。")

def judgeNextPage(browser):
    try:
        browser.find_by_xpath('//*[@id="pnnext"]').click()
        return 1
    except AttributeError as e: # 沒有下一頁了！
        print("沒有下一頁了，準備關閉瀏覽器。", e)
        pass


def getPageInARow(url, searchword, firstPage, topTabList, elementUrl):

    browser = buildSplinterBrowser("chrome")
     
    browser.visit(url)
    browserWaitTime(browser)

    searchwordKeyInAndEnter(browser, searchword)
    browser.driver.set_window_size(1024,768)

    forSureNws = findOutNws(browser, topTabList)

    keyNews = [key for key in forSureNws if forSureNws[key] == '新聞'].pop()
    # 擬人化mouse_over要排除新聞tab
    topTabList.remove(int(keyNews))

    print(f"點擊 {keyNews} 去到 新聞頁")
    #點擊新聞tab
    browser.find_by_xpath(f'//*[@id="hdtb-msb-vis"]/div[{keyNews}]/a').click()
    timeSleepRandomly()

    newsDict = {}
    newsDictInner = {}
    while True:
        print(f"進行 {searchword} 第", firstPage, "頁")
        elementUrlExtract(browser, topTabList, elementUrl, newsDictInner)
        judgment = judgeNextPage(browser)
        if judgment:
            print("仍有下一頁，繼續爬取！")
            firstPage += 1
            pass
        else:
            browser.quit()
            break

    
    newsDict["dateTime"] = timeStampGenerator()
    newsDict["keyword"] = searchword
    newsDict["newsTotalNum"] = len(newsDictInner)
    newsDict["newsUrl"] = newsDictInner

    return newsDict

   


if __name__ == '__main__':

    objectiveFolder = "rawData"
    objective = "news"

    searchword = "家電促銷"
    firstPage = 1

    topTabList = [row for row in range(2,6)] #新聞、圖片、地圖、影片、[更多]__xpath不同，無法準確mouse_over()
    elementUrl = [row for row in range(1,11)] #一頁有10個標的

    url = "https://www.google.com/"
    
    begin = timeCalculate()

    mkdirForRawData(objectiveFolder, objective, "google", keyword=searchword)

    newsDicT = getPageInARow(url, searchword, firstPage, topTabList, elementUrl)

    timeStamp = newsDicT["dateTime"]
    newsTotalNum = newsDicT["newsTotalNum"]
    with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/google/{searchword}/google_{timeStamp}_{newsTotalNum}_{searchword}.json", 'w', encoding='utf-8')as f:
        json.dump(newsDicT, f, indent=2, ensure_ascii=False)
    print("寫出！")

    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))