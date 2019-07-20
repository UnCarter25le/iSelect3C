# -*- coding:utf-8 -*-
"""
程式名稱：
程式描述：


備　　註：


    

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

from libs.multiProcessing import _googleSearchWord
from libs.manipulateDir import listSecondDirBelowFiles
from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.time import timeCalculate
from libs.time import timeStampGenerator


if __name__ == '__main__':

    objectiveFolder = "rawData"

    objective = "news"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/google"
    dirRouteWriteOut = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/newsIntegration"

    begin = timeCalculate()

    # eraseRawData(objectiveFolder, objective, "newsIntegration")
    mkdirForRawData(objectiveFolder, objective, "newsIntegration")

    dirRouteToFiles = listSecondDirBelowFiles(dirRoute)

    newsDict = {}
    newsDictInner = {}
    for file in dirRouteToFiles:
        with open(file) as f:
            inn = json.load(f)
        newsDictInner.update(inn['newsUrl'])
    
    timeStamp =  timeStampGenerator()
    newsTotalNum = len(newsDictInner)
    allSearchword = "^".join([row for row in _googleSearchWord])
    newsDict["dateTime"] = timeStamp
    newsDict["keyword"] = allSearchword
    newsDict["newsTotalNum"] = newsTotalNum
    newsDict["newsUrl"] = newsDictInner

    with open(dirRouteWriteOut + f"/news_{timeStamp}_{newsTotalNum}_{allSearchword}.json","w", encoding="utf-8") as f:
        json.dump(newsDict, f, indent=2, ensure_ascii=False)

    







