# -*- coding:utf-8 -*-
"""
程式名稱：
程式描述：

    1. 

    2. 

備　　註：

#
家電促銷
家電補助
家電特價

"""



from bs4 import BeautifulSoup
import multiprocessing as mp
import random
import sys
import os
import requests
import json
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 專案資料夾下第二層，用兩個path.dirname
sys.path.append(_BASE_PATH)


from libs.requests import _headers
from libs.time import timeSleepRandomly
from libs.time import timeCalculate
from libs.time import timeSleepOne
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

def humanSimulate(browser,  keyNews, topTabList):
    ranNum = random.choice(topTabList)
    print(ranNum,"================")
    browser.find_by_xpath(f'//*[@id="hdtb-msb-vis"]/div[{ranNum}]/a').mouse_over()
    timeSleepRandomly()
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    timeSleepOne()
    browser.execute_script('window.scrollTo(0,0);')  
    browser.find_by_xpath('//*[@id="logo"]/img').mouse_over()

def elementUrlExtract(browser, keyNews, topTabList, elementUrl, newsDict):
    try:
        for order in elementUrl:
            broUrl = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/h3/a')
            broPublisher = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/div[1]/span[1]')
            broDate = browser.find_by_xpath(f'//*[@id="rso"]/div/div[{order}]/div/div/div[1]/span[3]')
            newsUrl = broUrl["href"]
            publisher = broPublisher.text
            date = broDate.text
            print(newsUrl)
            print(publisher)
            print(date)
            # timeSleepOne()
            timeSleepRandomly()
            newsDict[newsUrl] = [publisher.replace(" ",""), date]
            humanSimulate(browser, keyNews, topTabList)
            
    except AttributeError as e: # 新聞標的不到10項時。
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


def getPageInARow(url, topTabList, elementUrl):

    browser = buildSplinterBrowser("chrome")
     
    browser.visit(url)
    browserWaitTime(browser)

    searchwordKeyInAndEnter(browser, "家電促銷")
    browser.driver.set_window_size(1024,768)

    forSureNws = findOutNws(browser, topTabList)

    keyNews = [key for key in forSureNws if forSureNws[key] == '新聞'].pop()
    # 擬人化mouse_over要排除新聞tab
    topTabList.remove(int(keyNews))
    #加入『更多』
    topTabList.append(6)

    print(f"點擊 {keyNews} 去到 新聞頁")
    #點擊新聞tab
    browser.find_by_xpath(f'//*[@id="hdtb-msb-vis"]/div[{keyNews}]/a').click()
    timeSleepRandomly()

    newsDict = {}
    while True:
        elementUrlExtract(browser, keyNews, topTabList, elementUrl, newsDict)
        judgment = judgeNextPage(browser)
        if judgment:
            print("仍有下一頁，繼續爬取！")
            pass
        else:
            break
    else:
        print("break happen！5566")
    
    return newsDict

   


if __name__ == '__main__':

    objectiveFolder = "rawData"

    objective = "news"

    topTabList = [row for row in range(2,6)] #新聞、圖片、地圖、影片、[更多]

    elementUrl = [row for row in range(1,11)]

    url = "https://www.google.com/"
    
    begin = timeCalculate()

    mkdirForRawData(objectiveFolder, objective, "google")

    #共同佇列
    # keyword_queue = mp.JoinableQueue()

    #啟動進程
    #主進程

    newsDicT = getPageInARow(url, topTabList, elementUrl)

    with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/google/5566.json", 'w', encoding='utf-8')as f:
        json.dump(newsDicT, f, indent=2, ensure_ascii=False)
    print("寫出！")


    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))





