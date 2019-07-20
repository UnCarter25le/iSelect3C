# -*- coding:utf-8 -*-

"""
程式名稱：
程式描述：


備　　註：

    

"""
import os
import sys
import json
import jieba
import math

from collections import Counter
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)


from libs.mining import stopwordsLoad
from libs.mining import wantedwordsLoad
from libs.mining import _newsUrlCheckList
from libs.regex import searchWordTrueOrFalse
from libs.time import timeStampGenerator
from libs.manipulateDir import mkdirForCleanData


if __name__ == '__main__':

    objectiveFolder = "rawData"

    objectiveFolderClean = "cleanData"

    objectiveFolderDataMining = "dataMining"
    
    objectiveFolderDictionary = "dictionary"

    objective = "news"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/newsIntegration"

    fileName = os.listdir(dirRoute).pop()
    

    # counterNum = Counter()

    with open(dirRoute + "/" + fileName)as f:
        inn = json.load(f)

    newsObject = inn["newsUrl"]
    newsString = ""

    with open(f"{_BASE_PATH}/{objectiveFolderDataMining}/{objectiveFolderDictionary}/TFIDF_resultOfNewsTitle.json") as f:
        resultOfTFIDF = json.load(f)
    
    newsTitleCheckList = [row[0] for row in resultOfTFIDF]


    readyLink = {}
    for key in newsObject:
        #首先過濾出鎖定的新聞連結：
        for checkLink in _newsUrlCheckList:
            if searchWordTrueOrFalse(checkLink, key):
                linkResult = 1
                break
            else:
                linkResult = 0
                pass
        # 如果是鎖定的連結的話，以TFIDF重要的詞來正規匹配新聞標題，只要重要的詞命中，那麼該連結就放進字典。
        if linkResult:
            for checkWord in newsTitleCheckList:
                if searchWordTrueOrFalse(checkWord, newsObject[key][0]):
                    # [url : title]
                    readyLink[key] = newsObject[key][0]
                    break
        else:
            pass
    # for row in readyLink:            
    #     print(readyLink[row])
    # print(len(readyLink))

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
    keyword = inn["keyword"]
    newsObjectWhole["dateTime"] = timeStamp
    newsObjectWhole["keyword"] = keyword
    newsObjectWhole["newsTotalNum"] = totalNum
    newsObjectWhole["newsUrl"] = newsObjectReadyForCrawling


    mkdirForCleanData(objectiveFolderClean, objective)
    with open(f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}/googleNews_{timeStamp}_{totalNum}_{keyword}.json", "w", encoding="utf-8")as f:
        json.dump(newsObjectWhole, f, indent=2, ensure_ascii=False)






