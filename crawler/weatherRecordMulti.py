# -*- coding:utf-8 -*-
"""
程式名稱：
程式描述：

    1. 

    <tr>
    <th headers="subH-1">阿里山</th>                 測站

                                                    攝氏溫度
    <td headers="H-1 subH-2">12.5</td>              平均
    <td headers="H-1 subH-3">19.5/14</td>           最高溫度/當月日期
    <td headers="H-1 subH-4">8.1/5</td>             最低溫度/當月日期
    <td headers="H-1 subH-5">1105.5</td>            雨量毫米

                                                    風速 (公尺/秒)/風向(360°)/當月日期
    <td headers="H-1 subH-6">5.4/250.0/18</td>      最大十分鐘風
    <td headers="H-1 subH-7">13.8/300.0/18</td>     最大瞬間風

                                                    相對溼度(%)
    <td headers="H-1 subH-8">96</td>                平均
    <td headers="H-1 subH-9">46/14</td>             最小/當月日期

    <td headers="H-1 subH-10">764.1</td>            測站氣壓(百帕)

                                                    降水日數 >=0.1毫米
    <td headers="H-1 subH-11">26</td>               天

    <td headers="H-1 subH-12">49.1</td>             日照時數(小時)
    </tr>
    <tr>

    2. 

備　　註：

#old
https://www.cwb.gov.tw/V7/climate/monthlyData/mD.htm
#new
https://www.cwb.gov.tw/V8/C/C/Statistics/monthlydata.html
#API  ID時間不影響資料取得
https://www.cwb.gov.tw/V8/C/C/Statistics/MonthlyData/MOD/2019_5.html
https://www.cwb.gov.tw/V8/C/C/Statistics/MonthlyData/MOD/2019_5.html?ID=Mon%20Jun%2010%202019%2014:29:57%20GMT+0800%20(Taipei%20Standard%20Time)
https://www.cwb.gov.tw/V8/C/C/Statistics/MonthlyData/MOD/2019_5.html?ID=Mon Jun 10 2019 14:29:57 GMT+0800 (Taipei Standard Time)


process_1 x5  process_2 x 20 ，完成！一共耗時：29.163750410079956 秒


"""

from bs4 import BeautifulSoup
import multiprocessing as mp
import sys
import os
import requests
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 專案資料夾下第二層，用兩個path.dirname
sys.path.append(_BASE_PATH)

from libs.requests import _headers
from libs.time import timeSleepRandomly
from libs.time import timeCalculate
from libs.time import timeSleepOne
from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.multiProcessing import _weatherRecordAvailable
from libs.multiProcessing import distributeKeyword



def distributeMonthAvailable(input, output, _weatherRecordAvailable, objectiveFolder, objective, *args):
    begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        year = input.get()
        monthsAvailable = _weatherRecordAvailable[year]

        eraseRawData(objectiveFolder, objective, year)
        mkdirForRawData(objectiveFolder, objective, year)

        for month in monthsAvailable:
            consecutiveData = year + "+" + month
            output.put(consecutiveData)
            print(f'這裡是distributeMonthAvailable，準備送給  getPageInARow  處理: {year}年_{month}月 ')
        input.task_done()
        end = timeCalculate()
        print(f'{thisPID}_distributeMonthAvailable 累計耗時：{0} 秒'.format(end-begin))
        timeSleepOne()
        
def getPageInARaw(input, _headers, objectiveFolder, objective, *args):
    begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        consecutiveUrl = input.get()
        year, month = consecutiveUrl.split("+")

        url = f"https://www.cwb.gov.tw/V8/C/C/Statistics/MonthlyData/MOD/{year}_{month}.html"
        res = requests.get(url, headers=_headers)
        timeSleepRandomly()
        res.encoding = "utf-8"

        soup = BeautifulSoup(res.text,'html.parser')

        with open(f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{year}/{year}_{month}.txt", 'w', encoding='utf-8')as f:
            f.write(str(soup))
        print()
        print(f'{thisPID}  成功寫出  {year}_{month}.txt ')

        input.task_done()
        end = timeCalculate()
        print(f'{thisPID}_getPageInARaw 累計耗時：{0} 秒'.format(end-begin))
        timeSleepOne()


if __name__ == '__main__':

    objectiveFolder = "rawData"

    objective = "weather"

    begin = timeCalculate()
    
    #共同佇列宣告
    year_queue = mp.JoinableQueue()
    month_queue = mp.JoinableQueue()

    #啟動進程
    Process_1 = []
    for p in range(5):
        distributeMonthAvailable_proc = mp.Process(target=distributeMonthAvailable, args=(year_queue, month_queue, _weatherRecordAvailable, objectiveFolder, objective,))
        distributeMonthAvailable_proc.daemon = True
        distributeMonthAvailable_proc.start()
        print(f'建立第{p}個 distributeMonthAvailable_proc, {distributeMonthAvailable_proc}')
        Process_1.append(distributeMonthAvailable_proc)


    Process_2 = []
    for w in range(20):
        getPageInARaw_proc = mp.Process(target=getPageInARaw, args=(month_queue, _headers, objectiveFolder, objective,))
        getPageInARaw_proc.daemon = True
        getPageInARaw_proc.start()
        print(f'建立第{w}個 getPageInARaw_proc, {getPageInARaw_proc}')
        Process_2.append(getPageInARaw_proc)

    #主進程
    distributeKeyword(_weatherRecordAvailable, year_queue)
    print("=============main process distributeKeyword 已經完成任務了。=============")


    #通知main process 完成事情。 寫超過兩個queue，程式將無法正常終止。
    year_queue.join()
    month_queue.join()
    print('Multiprocessing has done all jobs!')
    

    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')
    for proc in Process_2:
        proc.terminate()
        print(f'{proc} has terminated!')

    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))
