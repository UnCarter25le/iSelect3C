# -*- coding:utf-8 -*-
"""
程式名稱：weatherRecordMunging.py
程式描述：


備　　註：

    
    
2014_11月   五分山雷達站  完全沒資料
裡是distributeKeyword，準備送給  接下來的進程  處理: /home/bluevc/2019/iSelect3C/dataMungingMultiWay/rawData/weather/2014/11_2014.txt
dataMungingMultiWay is in new process <Process(Process-1, started daemon)>, 21820 

Process Process-1:
Traceback (most recent call last):
  File "/home/bluevc/.pyenv/versions/3.6.8/lib/python3.6/multiprocessing/process.py", line 258, in _bootstrap
    self.run()
  File "/home/bluevc/.pyenv/versions/3.6.8/lib/python3.6/multiprocessing/process.py", line 93, in run
    self._target(*self._args, **self._kwargs)
  File "/home/bluevc/2019/iSelect3C/dataMungingMultiWay/weatherRecordMunging.py", line 72, in dataMungingMultiWay
    weatherRecordDict["temperatureHigh"] = numsHandler.searchFloatNums(weatherRecord.selectColumn(row, 1))
  File "/home/bluevc/2019/iSelect3C/libs/regex.py", line 190, in searchFloatNums
    number = searchNum.search(bookurl).group()
AttributeError: 'NoneType' object has no attribute 'group'
    


2013-5   新屋   沒有資料！

"""


import os
import sys
import json
from bs4 import BeautifulSoup
import multiprocessing as mp

_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 專案資料夾下第二層，用兩個path.dirname
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.manipulateDir import (
                        initialFileZeroUnderscoreInt,
                        listSecondDirBelowFiles,
                        mkdirForCleanData,
                        eraseCleanData
                        )
from libs.munging import weatherRecordMunging

from libs.timeWidget import (
                            timeCalculate,
                            timeStampGenerator,
                            timeSleepOne
                            )

from libs.multiProcessing import (
                            distributeKeyword
                                )
from libs.regex import numsHandler


# def dataMungingMultiWay(input, *args):
#     thisPID = os.getpid()
#     while True:
#         print(thisPID,"===========================================")
#         fileRoute = input.get()
#         print('dataMungingMultiWay is in new process %s, %s ' % (dataMungingMultiWay_proc, thisPID))
#         print()
        
#         with open(fileRoute)as f:
#             inn = f.read()
#         if not inn:
#             print("沒有天氣資料可以清洗。。。。。。\n"*10)
#             break
#         textSoup = BeautifulSoup(inn, "html.parser")

#         month, year = weatherRecord.generateDateFromFileRoute(fileRoute)
#         keyword = f"{year}-{month}"
#         dateTime = timeStampGenerator()

#         weatherDict = {}
#         weatherRecordArray = []
#         everyStationData = textSoup.select("tr")
#         for row in everyStationData:
#             weatherRecordDict = {}
#             try:
#                 weatherRecordDict["stationName"] = weatherRecord.selectStationName(row)
#                 weatherRecordDict["temperatureAverage"] = weatherRecord.selectColumn(row, 0)
#                 weatherRecordDict["temperatureHigh"] = numsHandler.searchFloatNums(weatherRecord.selectColumn(row, 1))
#                 weatherRecordDict["temperatureHighDate"] = weatherRecord.composeDate(year, month, row, 1)
#                 weatherRecordDict["temperatureLow"] = numsHandler.searchFloatNums(weatherRecord.selectColumn(row, 2))
#                 weatherRecordDict["temperatureLowDate"] = weatherRecord.composeDate(year, month, row, 2)
#                 weatherRecordDict["relativeHumidityAverage"] = weatherRecord.selectColumn(row, 6)
#                 weatherRecordDict["relativeHumidityLow"] = numsHandler.searchFloatNums(weatherRecord.selectColumn(row, 7))
#                 weatherRecordDict["relativeHumidityLowDate"] = weatherRecord.composeDate(year, month, row, 7)
#                 weatherRecordDict["rainful"] = weatherRecord.selectColumn(row, 3)
#                 weatherRecordDict["rainingDays"] = weatherRecord.selectColumn(row, 9)

#                 weatherRecordArray.append(weatherRecordDict)
#             except AttributeError as e:
#                 print("error code:", e)
#                 print(f"{keyword}   {weatherRecord.selectStationName(row)}   沒有資料！")
#                 print()
#                 continue

#         weatherDict["keyword"] = keyword
#         weatherDict["dateTime"] = dateTime
#         weatherDict["records"] = weatherRecordArray

#         with open(weatherRecord._dirRouteMungingClean + weatherRecord._weather + f"/weather_{keyword}_{dateTime}.json", 'w')as f:
#             json.dump(weatherDict, f, indent=2, ensure_ascii=False)

#         print("===========清洗完成=============")
#         print(f"這裡是dataMungingMultiWay_{thisPID}，準備完成工作。 ")
#         print()
#         end = timeCalculate()
#         print('dataMungingMultiWay 累計耗時：{0} 秒'.format(end-begin))
#         input.task_done()  #通知main process此次的input處理完成！
#         timeSleepOne() #暫停幾秒來模擬現實狀況。




def dataMunging(fileRouteGenerator):
    weatherDictOutter = {}
    weatherArrayOutter = []

    for fileRoute in fileRouteGenerator:
        with open(fileRoute)as f:
            inn = f.read()
        if not inn:
            print("沒有天氣資料可以清洗。。。。。。\n"*10)
            continue

        textSoup = BeautifulSoup(inn, "html.parser")

        month, year = weatherRecord.generateDateFromFileRoute(fileRoute)
        keyword = f"{year}-{month}"
        
        weatherDict = {}
        weatherRecordArray = []
        everyStationData = textSoup.select("tr")
        for row in everyStationData:
            weatherRecordDict = {}
            try:
                weatherRecordDict["stationName"] = weatherRecord.selectStationName(row)
                weatherRecordDict["temperatureAverage"] = weatherRecord.selectColumn(row, 0)
                weatherRecordDict["temperatureHigh"] = numsHandler.searchFloatNums(weatherRecord.selectColumn(row, 1))
                weatherRecordDict["temperatureHighDate"] = weatherRecord.composeDate(year, month, row, 1)
                weatherRecordDict["temperatureLow"] = numsHandler.searchFloatNums(weatherRecord.selectColumn(row, 2))
                weatherRecordDict["temperatureLowDate"] = weatherRecord.composeDate(year, month, row, 2)
                weatherRecordDict["relativeHumidityAverage"] = weatherRecord.selectColumn(row, 6)
                weatherRecordDict["relativeHumidityLow"] = numsHandler.searchFloatNums(weatherRecord.selectColumn(row, 7))
                weatherRecordDict["relativeHumidityLowDate"] = weatherRecord.composeDate(year, month, row, 7)
                weatherRecordDict["rainful"] = weatherRecord.selectColumn(row, 3)
                weatherRecordDict["rainingDays"] = weatherRecord.selectColumn(row, 9)

                weatherRecordArray.append(weatherRecordDict)
            except AttributeError as e:
                print("error code:", e)
                print(f"{keyword}   {weatherRecord.selectStationName(row)}   沒有資料！")
                print()
                weatherRecordDict["stationName"] = weatherRecord.selectStationName(row)
                weatherRecordDict["temperatureAverage"] = "0.0"
                weatherRecordDict["temperatureHigh"] = "0.0"
                weatherRecordDict["temperatureHighDate"] = "1970-01-01"
                weatherRecordDict["temperatureLow"] = "0.0"
                weatherRecordDict["temperatureLowDate"] = "1970-01-01"
                weatherRecordDict["relativeHumidityAverage"] = "0"
                weatherRecordDict["relativeHumidityLow"] = "0"
                weatherRecordDict["relativeHumidityLowDate"] = "1970-01-01"
                weatherRecordDict["rainful"] = "0.0"
                weatherRecordDict["rainingDays"] = "0"

                weatherRecordArray.append(weatherRecordDict)
                
        #取完一份txt的資料了，進行整裝
        weatherDict["keyword"] = keyword
        weatherDict["records"] = weatherRecordArray
        weatherArrayOutter.append(weatherDict)

        print(f"===========清洗完成  {keyword} =============")


    dateTime = timeStampGenerator()
    weatherDictOutter["latestDate"] = keyword
    weatherDictOutter["dateTime"] = dateTime
    weatherDictOutter["recordsArray"] = weatherArrayOutter
    with open(weatherRecord._dirRouteMungingClean + weatherRecord._weather + f"/weather_{dateTime}_{keyword}.json", 'w')as f:
        json.dump(weatherDictOutter, f, indent=2, ensure_ascii=False)

    
        
if __name__ == '__main__':

    weatherRecord = weatherRecordMunging()
    # fileRouteList = [f for f in listSecondDirBelowFiles(weatherRecord._dirRouteMungingRaw + weatherRecord._weather)]
    
    fileRouteGenerator = listSecondDirBelowFiles(weatherRecord._dirRouteMungingRaw + weatherRecord._weather)




    begin = timeCalculate()
    eraseCleanData(weatherRecord._objectiveFolderCleanData, weatherRecord._weather)
    mkdirForCleanData(weatherRecord._objectiveFolderCleanData, weatherRecord._weather)
    
    dataMunging(fileRouteGenerator)






    #共同佇列宣告
    # file_queue = mp.JoinableQueue()

    # 啟動進程
    # Process_1 = []
    # for p in range(3):
    #     dataMungingMultiWay_proc = mp.Process(target=dataMungingMultiWay, args=(file_queue,))
    #     dataMungingMultiWay_proc.daemon = True
    #     dataMungingMultiWay_proc.start()
    #     print(f'建立第{p}個 dataMungingMultiWay_proc, {dataMungingMultiWay_proc}')
    #     Process_1.append(dataMungingMultiWay_proc)

    #主進程
    # distributeKeyword(fileRouteList, file_queue)
    # print("=============main process distributeKeyword 已經完成任務了。=============")

    #通知main process 完成事情。 寫超過兩個queue，程式將無法正常終止。
    # file_queue.join()    
    # print('Multiprocessing has done all jobs!')
    

    # for proc in Process_1:
    #     proc.terminate()
    #     print(f'{proc} has terminated!')





    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))







