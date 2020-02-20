# -*- coding:utf-8 -*-

"""
程式名稱：selectedNewsMulti.py
程式描述：


備　　註：

   

花費： 1282.5719978809357 秒
"""



import os
import sys
import json
import multiprocessing as mp
from collections import Counter

_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)

from libs.mining import newsMining
from libs.munging import rawDataMunging
from libs.timeWidget import (
                           timeStampGenerator,
                           timeCalculate)
from libs.sqlDMLAndsqlAlchemyORM import selectedNewsContentMunging
from libs.manipulateDir import mkdirForCleanData


if __name__ == '__main__':

   newsMining = newsMining()

   mkdirForCleanData(rawDataMunging._objectiveFolderCleanData, rawDataMunging._objectiveFolderNewsWithContent)

   dirRoute = f"{rawDataMunging._dirRouteMungingClean}{rawDataMunging._objectiveFolderNews}/"


   begin = timeCalculate()

   fileName, fileNums = newsMining.judgeFolderFiles(dirRoute)

   referenceFile = selectedNewsContentMunging().loadReferenceFileIn()

   if fileNums == 0:
      print("""
            尚未有clean的newsUri可以爬！請先完成
            googleNewsMulti.py --> 
            newsMunging.py --> 
            jiebaForNewsTitle.py --> 
            copewithNewsUrlForCrawling.py
            """)

   elif fileNums == 1:
      print("處理最新檔案(一個)：", fileName[0])
      latestFileJson = newsMining.loadOneFileIn(dirRoute + fileName[0])
      
      readyLinkObject = latestFileJson["newsUrl"]


      newsDictOutter = {}
      newsDictInner = {}

      for newsLink in readyLinkObject:
         publisher_Id, publisher, videoLinkInContent, newsContent = newsMining.judgeHowToCrawl(newsLink, referenceFile)

         if publisher and newsContent: #被捕捉到的新聞才做處理
            newsTitle = readyLinkObject[newsLink][0]
            publishDate = readyLinkObject[newsLink][2]   
            # 組裝json
            newsDictInner[newsLink] = {"newsTitle":newsTitle,
                                       "publisher":publisher,
                                       "publisher_Id":publisher_Id,
                                       "publishDate":publishDate,
                                       "videoLinkInContent":videoLinkInContent,
                                       "newsContent":newsContent}
            
         elif publisher and not newsContent:# 爬取錯誤的處理
            newsTitle = readyLinkObject[newsLink][0]
            publishDate = readyLinkObject[newsLink][2]   
            # 組裝json
            newsDictInner[newsLink] = {"newsTitle":newsTitle,
                                       "publisher":publisher,
                                       "publisher_Id":publisher_Id,
                                       "publishDate":publishDate,
                                       "videoLinkInContent":videoLinkInContent,
                                       "newsContent":newsContent}
      
      dataTime = latestFileJson["dateTime"] # 這裡的時間同標題篩選過後的檔案的dateTime
      keyword = latestFileJson["keyword"]
      newsTotalNum = len(newsDictInner)

      newsDictOutter["dateTime"] = dataTime
      newsDictOutter["keyword"] = keyword
      newsDictOutter["newsTotalNum"] = newsTotalNum
      newsDictOutter["newsUrl"] = newsDictInner

      with open(f"{rawDataMunging._dirRouteMungingClean}{rawDataMunging._objectiveFolderNewsWithContent}/googleNews_{dataTime}_{newsTotalNum}_{keyword}.json", "w", encoding="utf-8")as f:
         json.dump(newsDictOutter, f, indent=2, ensure_ascii=False)
      
      print(f"寫出檔案： googleNews_{dataTime}_{newsTotalNum}_{keyword}.json" )

   else:

      latestFileName =  fileName[-1]
      forCheckFileName = fileName[-2]
      latestFileJson = newsMining.loadOneFileIn(dirRoute + latestFileName)
      forCheckFileJson = newsMining.loadOneFileIn(dirRoute + forCheckFileName)

      latestFileSet = set(latestFileJson["newsUrl"])
      forCheckFileSet = set(forCheckFileJson["newsUrl"])

      
      print("最新檔案", latestFileName, "的新聞數：", len(latestFileSet))
      print("上回檔案", forCheckFileName, "的新聞數：", len(forCheckFileSet))
      # in-place差集
      latestFileSet.difference_update(forCheckFileSet)
      leftRemaining = len(latestFileSet)

      if leftRemaining:
         differenceDict = {url: latestFileJson["newsUrl"][url] for url in latestFileSet}
         
         print(len(differenceDict), latestFileSet)

         # for newsLink in differenceDict:
         #    publisher_Id, publisher, newsContent = newsMining.judgeWhichLinkToCrawl(newsLink, referenceFile)

         newsDictOutter = {}
         newsDictInner = {}

         for newsLink in differenceDict:
            # debug
            # if newsLink != "https://udn.com/news/story/7238/3600804":
            #    continue
            
            publisher_Id, publisher, videoLinkInContent, newsContent = newsMining.judgeHowToCrawl(newsLink, referenceFile)

            
            if publisher and newsContent == "404_None":# 新聞內容404
               """
               此新聞原先爬的到，但目前20200207爬不到，為避免將原先的新聞內容
               覆蓋成None，因此這邊要以contine處理。
               
               "https://udn.com/news/story/7238/3600804": [
               "經濟部家電補助台東：勢必向中央爭取經費",
               "udn聯合新聞網",
               "2019-01-17"
               """
               newsTitle = differenceDict[newsLink][0]
               print(newsTitle, " 網頁404! ", newsLink)
               continue
            
            elif publisher and newsContent: #被捕捉到的新聞才做處理
               newsTitle = differenceDict[newsLink][0]
               publishDate = differenceDict[newsLink][2]   
               # 組裝json
               newsDictInner[newsLink] = {"newsTitle":newsTitle,
                                       "publisher":publisher,
                                       "publisher_Id":publisher_Id,
                                       "publishDate":publishDate,
                                       "videoLinkInContent":videoLinkInContent,
                                       "newsContent":newsContent}
            
            elif publisher and not newsContent:# 爬取錯誤的處理
               newsTitle = differenceDict[newsLink][0]
               publishDate = differenceDict[newsLink][2]   
               # 組裝json
               newsDictInner[newsLink] = {"newsTitle":newsTitle,
                                       "publisher":publisher,
                                       "publisher_Id":publisher_Id,
                                       "publishDate":publishDate,
                                       "videoLinkInContent":videoLinkInContent,
                                       "newsContent":newsContent}
         
         dataTime = latestFileJson["dateTime"] # 這裡的時間同標題篩選過後的檔案的dateTime
         keyword = latestFileJson["keyword"]
         newsTotalNum = len(newsDictInner)

         newsDictOutter["dateTime"] = dataTime
         newsDictOutter["keyword"] = keyword
         newsDictOutter["newsTotalNum"] = newsTotalNum
         newsDictOutter["newsUrl"] = newsDictInner

         with open(f"{rawDataMunging._dirRouteMungingClean}{rawDataMunging._objectiveFolderNewsWithContent}/googleNews_{dataTime}_{newsTotalNum}_{keyword}.json", "w", encoding="utf-8")as f:
            json.dump(newsDictOutter, f, indent=2, ensure_ascii=False)

         print(f"寫出檔案： googleNews_{dataTime}_{newsTotalNum}_{keyword}.json" )

      else:
         print("無須爬蟲！")
    

   end = timeCalculate()
   print("花費：", end-begin, "秒。")