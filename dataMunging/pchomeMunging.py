# -*- coding:utf-8 -*-
"""
程式名稱： 以關鍵搜索字清洗pchome爬蟲的結果。
程式描述：

    指定 searchword ，就可以清洗pchome 下載下來的raw data。

備　　註：

    

    需要捕捉的欄位：
    "pics"、"picb"、"name"、originprice"、"Id"、"produrl"

    還未把非真正冷氣空調的去掉。

"""
import os
import sys
import json
import datetime
import sqlalchemy as sqla
_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)

from libs.munging import EcommerceDataProcessToSet
from libs.multiProcessing import _pchomeKeywordUrlPair
from libs.timeWidget import timeStampGenerator
from libs.manipulateDir import (
                                initialFile,
                               mkdirForCleanData
                                )
from libs.sqlDDLAndsqlAlchemyORM import (
                                        sqlObjectInitail,
                                        sqlORMForTables
                                        )


    


def mungingPchome(_BASE_PATH, searchword, objectiveFolder, objectiveFolderClean, objective):
    
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/"
    dir1 = dirRoute + "24h/"
    dir2 = dirRoute + "vdr/"
    dir3 = dirRoute + "kdn/"

    pchomeDict = {}
    productArray = []
    # pchomeDict["picurl"] = "https://d.ecimg.tw"
    # pchomeDict["produrl"] = "https://24h.pchome.com.tw/prod/"
    pchomeDict["keyword"] = f"{searchword}(24h_vdr_kdn)"
    pchomeDict["dateTime"] = timeStamp

    for directory in [dir1, dir2, dir3]:
        if initialFile(directory): #有些資料夾下面沒有檔案
            for file in initialFile(directory):
                with open(directory + file)as f:
                    inn = json.load(f)

                # 處理soup=""的情況
                if not inn:
                    continue

                for fileinner in inn['prods']:
                    productDict = {}
                    productDict['Id'] = fileinner['Id']
                    productDict['name'] = fileinner['name']
                    productDict['originprice'] = fileinner['originPrice']
                    productDict['pics'] = 'https://d.ecimg.tw'+fileinner['picS']
                    productDict['picb'] = 'https://d.ecimg.tw'+fileinner['picB']
                    productDict["produrl"] = "https://24h.pchome.com.tw/prod/" + fileinner["Id"]
                    productArray.append(productDict)
    # 每一個搜索字下的3個資料夾中，每個json檔案的 'prods' 陣列資料都append後，再統一指定。
    pchomeDict['product'] = productArray

    source = '_'.join([dirname.split('/')[-2] for dirname in [dir1, dir2, dir3]])

    print(f"===========進行 {searchword}(24h_vdr_kdn) 去重=============")

    pchomeDict['product'], setNums = EcommerceDataProcessToSet(pchomeDict['product'])

    mkdirForCleanData(objectiveFolderClean, objective)

    with open(f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}/pchome_{source}_{timeStamp}_{setNums}_{searchword}.json", 'w')as f:
        json.dump(pchomeDict, f, indent=2, ensure_ascii=False)

    print(f"===========完成 {searchword}(24h_vdr_kdn) 清洗！=============")

    # print(f"===========開始 {searchword}(24h_vdr_kdn) 資料 INSERT！=============")
    




if __name__ == '__main__':

    objectiveFolder = "rawData"

    objectiveFolderClean = "cleanData"

    objective = "pchome"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/"

    timeStamp = timeStampGenerator()

    tableClassBase = sqlObjectInitail()._tableClassBase
    engine = tableClassBase.connectToMySQLEngine()

    # 清洗
    for searchword in _pchomeKeywordUrlPair:
        mungingPchome(_BASE_PATH, searchword, objectiveFolder, objectiveFolderClean, objective)

    # in

    