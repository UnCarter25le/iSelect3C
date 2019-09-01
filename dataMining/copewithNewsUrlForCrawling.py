# -*- coding:utf-8 -*-

"""
程式名稱：
程式描述：


備　　註：

    

"""
import json
import math
import os
import sys

_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)

from libs.manipulateDir import (
                            mkdirForCleanData,
                            initialFileFirstUnderscoreString
                            )
from libs.mining import (
                        _newsUrlCheckList,
                        newsMining
                        )
from libs.regex import searchWordTrueOrFalse
from libs.timeWidget import timeStampGenerator


def loadNewsIntegration():
    with open(dirRoute + "/" + fileName)as f:
        inn = json.load(f)
    return inn["keyword"], inn["newsUrl"]


def loadTFIDFResultOfNewsTitle():
    with open(f"{_BASE_PATH}/{objectiveFolderDataMining}/{objectiveFolderDictionary}/TFIDF_resultOfNewsTitle.json") as f:
        resultOfTFIDF = json.load(f)
    return resultOfTFIDF

if __name__ == '__main__':

    objectiveFolder = "rawData"

    objectiveFolderClean = "cleanData"

    objectiveFolderDataMining = "dataMining"
    
    objectiveFolderDictionary = "dictionary"

    objective = "news"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/newsIntegration"

    fileName = initialFileFirstUnderscoreString(dirRoute)[-1]
    print(fileName)


    # 提出所有的新聞標題
    # with open(dirRoute + "/" + fileName)as f:
    #     inn = json.load(f)
    # for key in inn["newsUrl"]:
    #     print(inn["newsUrl"][key][0])

    keyword, newsObject = loadNewsIntegration()
    newsString = ""

    resultOfTFIDF = loadTFIDFResultOfNewsTitle()
    newsTitleCheckList = [row[0] for row in resultOfTFIDF]

    

    # -----------------------------------------------------------------------------------------------------
    # 優化判斷
    # 1. 剔除非節能12類別的東西
    # 2. 剔除非「節能促銷」、「家電促銷」、「節能補助政策」、「家電補助政策」、「家電產業營收業績表現」相關的新聞；注意不要讓「公司股市表現、公司與公司競爭」等新聞入列
    # 3. 判定能決定新聞是否留存的關鍵字，例如：["春節", "年中慶", "週年慶", "父親節", "母親節", ... _lastCheckForUnwantedWords]，如出現陣列內的字，權重必須扣1。
    readyLink = {}
    # readyLinkComparison = {}
    for key in newsObject:
        #首先過濾出鎖定的新聞連結：
        for checkLink in _newsUrlCheckList:
            if searchWordTrueOrFalse(checkLink, key):
                linkResult = 1
                break
            else:
                linkResult = 0
                pass
        # 如果是鎖定的連結的話，以TFIDF重要的詞來正規匹配新聞標題，只要重要的詞命中(多次以上)，那麼該連結才可放進字典。
        if linkResult:
            targetNum = 0
            newsTitle = newsObject[key][0]
            for checkWord in newsTitleCheckList:
                if searchWordTrueOrFalse(checkWord, newsTitle):

                    # 只命中一次：
                    # readyLink[key] = newsTitle
                    # break
                    
                    # 要命中多次：
                    targetNum += 1
                    if targetNum == 3:
                        # 排除不希望有的字詞
                        for stopW in newsMining._lastCheckForUnwantedWords:
                            if searchWordTrueOrFalse(stopW, newsTitle):
                                targetNum -= 1
                                # readyLinkComparison[key] = newsTitle

                        if targetNum == 3:
                            readyLink[key] = newsTitle
                            targetNum = 0
                            break
        else:
            pass

    newsObjectWhole = {}
    newsObjectReadyForCrawling = {}
    for key in readyLink:
        try:
            newsObjectReadyForCrawling[key] = newsObject[key]
        except KeyError as e:
            newsObjectReadyForCrawling[key] = None
            print("擷取待爬取url出錯！", e)
    
    timeStamp = timeStampGenerator()
    totalNum = len(newsObjectReadyForCrawling)
    newsObjectWhole["dateTime"] = timeStamp
    newsObjectWhole["keyword"] = keyword
    newsObjectWhole["newsTotalNum"] = totalNum
    newsObjectWhole["newsUrl"] = newsObjectReadyForCrawling


    #-----------------------------------檢測判斷如何---------------------
    print("篩選出", len(readyLink), "則新聞。")
    # print(len(readyLinkComparison))
    # for row in readyLinkComparison:
    #     print(readyLinkComparison[row])

    newsTitleList = [newsObjectReadyForCrawling[key][0]+"\n" for key in newsObjectReadyForCrawling]
    with open(f"{_BASE_PATH}/{objectiveFolderDataMining}/{objectiveFolderDictionary}/threeWord.txt",'w')as f:
        f.writelines(newsTitleList)
        

    # ----------------------------------寫出成果------------------
    mkdirForCleanData(objectiveFolderClean, objective)
    with open(f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}/googleNews_{timeStamp}_{totalNum}_{keyword}.json", "w", encoding="utf-8")as f:
        json.dump(newsObjectWhole, f, indent=2, ensure_ascii=False)