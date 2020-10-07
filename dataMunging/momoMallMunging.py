# -*- coding:utf-8 -*-
"""
程式名稱：以關鍵搜索字清洗momomall爬蟲的結果。
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
from libs.munging import (
                        EcommerceDataProcessToSet, 
                        ecommerceMunging
                        )
from libs.timeWidget import timeSleepOne
# from math import ceil
# import time,json,os,re,random




#總頁數
#totalPage = interDiv(searchNums(textSoup.select_one('.totalTxt').text),30)


def dataMunging(input, dirRoute, objectiveFolderClean, objective, domainUrl):
    """
    "Id": "6631009",
      "name": "",
      "originprice": "NaN",
      "pics": "https://img1.momoshop.com.tw/goodsimg/0006/631/009/6631009_L.jpg?t=000",
      "picb": "None",
      "produrl": "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=6631009&Area=search&mdiv=403&oid=55_8&cid=index&kw=%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF"
    },
    
    有的商品有連結，但是價格與品名不全，要處理。

    {
      "Id": "6574471",
      "name": "【MITSUBISHI 三菱】16公升一級能效強力型除濕機(MJ-E160HN)",
      "originprice": "NaN",
      "pics": "https://img1.momoshop.com.tw/goodsimg/0006/574/471/6574471_L.jpg?t=000",
      "picb": "None",
      "produrl": "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=6574471&Area=search&mdiv=403&oid=3_22&cid=index&kw=%E9%99%A4%E6%BF%95%E6%A9%9F"
    }
    """
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
                products = textSoup.select_one("#prdListArea").select_one(".list").children
                for item in products:
                    innerDict = {}
                    innerDict['Id'] = item.attrs.get("id")#產品id

                    productName = item.find("p", {"class":"prdName"}).text#產品名稱
                    #現在價格
                    if item.find("p", {"class":"prdPrice"}).b.attrs.get("class"):
                        originprice = item.find("p", {"class":"prdPrice"}).select("b")[-1].text.replace(",", "").replace("$", "")
                    else:
                        originprice = item.find("p", {"class":"prdPrice"}).b.text.replace(",", "").replace("$", "")

                    #原價
                    # try:
                    #     originpriceFixed = item.find("p", {"class":"prdPrice"}).span.text
                    # except AttributeError as e:
                    #     originpriceFixed = "0"
                        # print("沒有原價")
                    #廠商名稱
                    # print(item.find("p", {"class":"companyName"}).text)
                    
                    if productName:
                        innerDict['name'] = productName

                        if originprice in ("NaN", "熱銷一空"):
                            innerDict['originprice'] = "0"  #"NaN"
                            # innerDict['originpriceFixed'] = "0"
                        else:
                            innerDict['originprice'] = originprice
                            # innerDict['originpriceFixed'] = originpriceFixed

                            
                    else:
                        innerDict['name'] = "品名抓不到"
                        innerDict['originprice'] = "0"  #"NaN"
                        # innerDict['originpriceFixed'] = "0"

                    innerDict['pics'] = item.img.attrs.get("src")#圖片連結
                    innerDict['picb'] = "None"
                    innerDict['produrl'] = item.a.attrs.get("href")#產品連結
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

        momoDict['product'], setNums = ecommerceMunging.EcommerceDataProcessToSet(momoDict['product'])

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

    objective = "momoMall"

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












