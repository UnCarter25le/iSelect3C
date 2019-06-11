# -*- coding:utf-8 -*-
"""
程式名稱：
程式描述：

    1. 

    2. 

備　　註：

#
http://e-service.cwb.gov.tw/HistoryDataQuery/

"""


from bs4 import BeautifulSoup
import requests
import os
import sys
import json
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 專案資料夾下第二層，用兩個path.dirname
sys.path.append(_BASE_PATH)

from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.manipulateDir import mkdirForCleanData



if __name__ == '__main__':

    objectiveFolder = "rawData"

    objectiveFolderClean = "cleanData"

    objective = "observationStation"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/"
    
    mkdirForCleanData(objectiveFolderClean, objective)

    directory = dirRoute + "overviewData/"

    fileInDirectory = os.listdir(directory)
    

    with open(directory + fileInDirectory[0])as f:
        inn = f.read()
    textSoup = BeautifulSoup(inn,"html.parser")

    detailData = textSoup.find('script',{"type":"text/javascript"}).text

    #replace掉很多『tab的空格』                                                                         一般空格            一個tab          兩個tab                   
    detailData = "{" + (detailData.split("var stList = {")[1].split("//console.log(stList);")[0].replace(" ","").replace("	","").replace("		","").replace("\n","").replace(";",""))
        
    JsondetailData  = json.loads(detailData)

    # print(JsondetailData)
    with open(f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}/observationStation.json", 'w', encoding='utf-8')as f:
        json.dump(JsondetailData, f, indent=2, ensure_ascii=False)

    print("成功寫出  observationStation.json")
    