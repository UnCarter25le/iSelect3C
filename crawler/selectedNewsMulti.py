# -*- coding:utf-8 -*-

"""
程式名稱：
程式描述：


備　　註：

   

"""



import os
import sys
import json
import multiprocessing as mp
from collections import Counter

_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)

from libs.mining import _newsUrlCheckDict
from libs.regex import searchWordTrueOrFalse


def judgeFolderFiles(dirRoute):
   fileName = os.listdir(dirRoute)
   if not fileName:
      return fileName, 0
   else:
      return fileName, len(fileName)

def loadOneFileIn(fileRoute):
   with open(fileRoute)as f:
      jsonFile = json.load(f)
   return jsonFile


if __name__ == '__main__':

      objectiveFolder = "rawData"

      objectiveFolderClean = "cleanData"

      objectiveFolderDataMining = "dataMining"

      objectiveFolderDictionary = "dictionary"

      objective = "news"

      dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}/"

      
      fileName, fileNums = judgeFolderFiles(dirRoute)

      if fileNums == 0:
         print("尚未有clean的newsUri可以爬！請先完成googleNewsMulti.py --> newsMunging.py --> jiebaForNewsTitle.py --> copewithNewsUrlForCrawling.py")
      elif fileNums == 1:
         latestFileJson = loadOneFileIn(dirRoute + fileName[0])
         
         readyLinkObject = latestFileJson["newsUrl"]

         for newsLink in readyLinkObject:
            for checkLink in _newsUrlCheckDict:
               if searchWordTrueOrFalse(checkLink, newsLink):
                  publisher = _newsUrlCheckDict.get(checkLink)
                  print(publisher)
                  break
               else:
                  pass
            
            if publisher == "udn聯合新聞網":
               pass
            elif publisher == "經濟日報":
               pass
            elif publisher == "自由時報電子報":
               pass
            elif publisher == "中時電子報":
               pass
            elif publisher == "蘋果日報":
               pass
            elif publisher == "Yahoo奇摩新聞":
               pass
            elif publisher == "ETtoday":
               pass
            elif publisher == "NOWnews":
               pass
            elif publisher == "TVBS新聞":
               pass

      else:
         #可按時間升冪排列
         fileName.sort(key= lambda x: x.split('_')[1])

         latestFile =  fileName[-1]
         forCheckFile = fileName[-2]
         latestFileJson = loadOneFileIn(dirRoute + latestFile)
         forCheckFileJson = loadOneFileIn(dirRoute + forCheckFile)

         latestFileSet = set(latestFileJson["newsUrl"])
         forCheckFileSet = set(forCheckFileJson["newsUrl"])

         
         print("最新檔案", latestFile, "的新聞數：", len(latestFileSet))
         print("上回檔案", forCheckFile, "的新聞數：", len(forCheckFileSet))
         # in-place差集
         latestFileSet.difference_update(forCheckFileSet)
         leftRemaining = len(latestFileSet)

         if leftRemaining:
            differenceDict = {url: latestFileJson["newsUrl"][url] for url in latestFileSet}
            
            
            print(len(differenceDict))
            # for url in differenceDict:
               

         else:
            print("無須爬蟲！")
    

