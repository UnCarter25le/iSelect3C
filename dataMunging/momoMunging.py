# -*- coding:utf-8 -*-
"""
程式名稱：以關鍵搜索字清洗momo爬蟲的結果。
程式描述：


備　　註：

    需要捕捉的欄位：
    "pics"、"picb"（設為None）、"name"、originprice"、"Id"、"produrl"

    

"""
from bs4 import BeautifulSoup
import os
import sys
import json
import datetime
import time
import multiprocessing as mp
_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)

from libs.manipulateDir import initialFileZeroUnderscoreInt
from libs.manipulateDir import mkdirForCleanData
from libs.regex import searchNums
from libs.regex import interDiv
from libs.multiProcessing import distributeKeyword
from libs.multiProcessing import _momoKeywordUrlPair
from libs.munging import EcommerceDataProcessToSet
from libs.timeWidget import timeSleepOne
# from math import ceil
# import time,json,os,re,random




#總頁數
#totalPage = interDiv(searchNums(textSoup.select_one('.totalTxt').text),30)


def dataMunging(input, dirRoute, objectiveFolderClean, objective, domainUrl):
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        searchword = input.get()
        
        mkdirForCleanData(objectiveFolderClean, objective)

        # '/home/bluevc/2019/iSelect3C/dataMunging/rawData/momo/冷暖空調電熱水瓶'  <---關鍵字累加的問題
        # dirRoute = dirRoute + searchword

        fileRoute = dirRoute + searchword
        
        if not os.listdir(fileRoute):
            print(f"============={objective} {searchword} 資料夾沒有東西，此進程準備結束。=============")
            input.task_done()
            timeSleepOne()
            print("========================break========================")
            break

        momoDict = {}
        productArray= [] 

        for file in initialFileZeroUnderscoreInt(fileRoute):
            # print("start " + file + " ! ")

            with open(fileRoute + "/" + file)as f:
                inn = f.read()

            # 處理soup=""的情況
            if not inn:
                continue
            textSoup = BeautifulSoup(inn,'html.parser')
            try:
                #一頁至多有30項
                products = textSoup.select_one('.listArea').select_one('ul').select('li')
                for item in products:
                    innerDict = {}
                    innerDict['Id'] = item.attrs.get('gcode')
                    innerDict['name'] = item.select_one('.goodsUrl').select_one('.prdName').text
                    innerDict['originprice'] = item.select_one('.goodsUrl').select_one('.money .price').text.replace('$','').replace(',','')
                    innerDict['pics'] = item.select_one('.goodsUrl img').attrs.get('src') 
                    innerDict['picb'] = "None"
                    innerDict['produrl'] = domainUrl + item.select_one('.goodsUrl').attrs.get('href')
                    productArray.append(innerDict)
            except Exception as e:
                print(f"{file} 有 {e} 的問題。")


        dateTime = datetime.datetime.now()
        fmt = "%Y-%m-%d-%H-%M"  #"%Y年%m月%d日%H時%M分"
        timeStamp = dateTime.strftime(fmt)

        momoDict['product'] = productArray
        momoDict['keyword'] = searchword
        momoDict["dateTime"] = timeStamp


        print("===========進行去重=============")

        momoDict['product'], setNums = EcommerceDataProcessToSet(momoDict['product'])

        with open(f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}/momo_{timeStamp}_{setNums}_{searchword}.json", 'w')as f:
            json.dump(momoDict, f, indent=2, ensure_ascii=False)

        print("===========清洗完成=============")
        print(f"這裡是dataMunging_{thisPID}，準備完成工作。 ")
        print()
        end = time.time()
        print('dataMunging 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()  #通知main process此次的input處理完成！
        timeSleepOne() #暫停幾秒來模擬現實狀況。

if __name__ == '__main__':


    domainUrl = "https://www.momoshop.com.tw"

    objectiveFolder = "rawData"

    objectiveFolderClean = "cleanData"

    objective = "momo"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/"

    begin = time.time()

    # 共同佇列宣告
    searchword_queue = mp.JoinableQueue()


    # 啟動進程
    Process_1 = []
    for p in range(3):
        dataMunging_proc = mp.Process(target=dataMunging, args=(searchword_queue, dirRoute, objectiveFolderClean, objective, domainUrl,))
        dataMunging_proc.daemon = True
        dataMunging_proc.start()
        print(f'建立第{p}個 dataMunging_proc, {dataMunging_proc}')
        Process_1.append(dataMunging_proc)
    
    # 主行程
    distributeKeyword(_momoKeywordUrlPair, searchword_queue)
    print("=============main process distributeKeyword 已經完成任務了。=============")

    #通知main process 完成事情。
    searchword_queue.join()

    print('Function dataMunging has done all jobs!')
    
    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')
    
    end = time.time()
    
    print("完成！一共耗時：{0} 秒".format(end-begin)) 












