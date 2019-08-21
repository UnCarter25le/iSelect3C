# -*- coding:utf-8 -*-

"""
程式名稱：bureauEnergyMulti_1.py

程式描述：

    1. 以『關鍵分類搜索字』爬蟲 經濟部能源局（經濟部能源局節能標章）https://ranking.energylabel.org.tw/product/Approval/list.aspx。

    _bureauEnergyKeywordUrlPair = {"無風管空氣調節機":"",
                        "除濕機" : (""),
                        "電冰箱" : (""),
                        "電熱水瓶" : (""),
                        "溫熱型開飲機" : (""),
                        "溫熱型飲水機" : (""),
                        "冰溫熱型開飲機" : (""),
                        "冰溫熱型飲水機" : (""),
                        "貯備型電熱水器": (""),
                        "瓦斯熱水器(即熱式燃氣熱水器)": (""),
                        "瓦斯爐(燃氣台爐)" : (""),
                        "安定器內藏式螢光燈泡": ("")}


    2. 

    input: _bureauEnergyKeywordUrlPair 的資訊。

    Output: 將每個類別的各頁 html，以txt形式儲存本地。見/dataMunging/bureauEnergy/關鍵字/overview/。

備　　註：

30個進程，完成！一共耗時：659.8574628829956 秒 。能源局官網上的類別12個都載下來。

"""


from bs4 import BeautifulSoup
import requests
# import time
import os
import sys
# import random
import json
import multiprocessing as mp

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)   # 因為此行生效，所以才能引用他處的module

from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.manipulateDir import initialFile
from libs.multiProcessing import distributeKeyword
from libs.multiProcessing import _bureauEnergyKeywordUrlPair
from libs.timeWidget import timeSleepRandomly
from libs.timeWidget import timeCalculate
from libs.timeWidget import timeSleepOne
from libs.httpRequests import _headers



def overviewUriDistributor(input, output, keywordUrlPair, headers, dirRoute,objectiveFolder, objective, *args):
    begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        searchword = input.get()
        url = keywordUrlPair[searchword]
        totalPage = getPageFirst(url + "1", headers)
        
        print('overviewUriDistributor is in new process %s, %s ' % (overviewUriDistributor_proc, os.getpid()))
        print('------接下來要發送 ' + searchword + ' 的overviewUri---------', '共' ,totalPage, '頁')

        #莫把檢查資料夾的工作放到爬蟲時才做，那樣會對資料夾開開刪刪。
        eraseRawData(objectiveFolder, objective, searchword, keyword="overview")
        mkdirForRawData(objectiveFolder, objective, searchword, keyword="overview")

        for page in range(1, int(totalPage)+1):
            correctUrl = url + str(page)

            readyTxtFileRoute = dirRoute + f"{searchword}/overview/{page}_{totalPage}_{searchword}.txt"
            #TypeError: must be str, not tuple
            consecutiveData = searchword + "+" + correctUrl + "+" + readyTxtFileRoute

            output.put(consecutiveData)
        print(f'這裡是 overviewUriDistributor_{thisPID}，準備送給  getPageInARow  處理 {totalPage} 頁的 overviewUri')
        print()            
            
        end = timeCalculate()
        print('overviewUriDistributor 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()  #通知main process此次的input處理完成！
        timeSleepOne() #暫停幾秒來模擬現實狀況。




def getPageFirst(url, headers):
    
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    
    timeSleepRandomly()
    
    soup  = BeautifulSoup(res.text,'html.parser')
    totalPage = soup.select('.Paging span')[-1].text
    
    return totalPage

    
def getPageInARow(input, headers, objectiveFolder, objective, *args):
    begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        consecutiveUrl = input.get()
        searchword, correctUrl, txtFileRoute = consecutiveUrl.split("+")

        fileName = txtFileRoute.split("/")[-1]
        page = fileName.split("_")[0]
        totalPage = fileName.split("_")[1]
        
        print('getPageInARow is in new process %s, %s ' % (getPageInARow_proc, os.getpid()))
        print('------接下來要處理 ' + searchword + '第' ,page, '頁---------共', totalPage, '頁')

        res = requests.get(correctUrl, headers=headers)
        res.encoding = 'utf-8'

        timeSleepRandomly()

        soup  = BeautifulSoup(res.text,'html.parser')

        with open(txtFileRoute, 'w', encoding='utf-8')as f:
            f.write(str(soup))
        print(f"成功寫出  {searchword}  第 {page} 頁， 共 {totalPage} 頁。")
        end = timeCalculate()
        print('getPageInARow 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()  #通知main process此次的input處理完成！
        timeSleepOne() #暫停幾秒來模擬現實狀況。


if __name__ == '__main__':
    

    headers = _headers
    
    begin = timeCalculate()

    objectiveFolder = "rawData"

    # objectiveFolderClean = "cleanData"

    objective = "bureauEnergy"
    
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/"
    
    # domainUrl = 'https://ranking.energylabel.org.tw/product/Approval/'

    print('-------------------------------------------------------------------------')

    #共同佇列
    keyword_queue = mp.JoinableQueue() # 發出關鍵字，讓接收關鍵字的進程接著發送更多的overviewUri。
    overviewUri_queue = mp.JoinableQueue()  #接收到overviewUri的進程爬取html。
    
    # 啟動進程
    Process_1 = []  #發送overviewUri，總計有12個分類
    for x in range(8):
        overviewUriDistributor_proc = mp.Process(target=overviewUriDistributor, args=(keyword_queue, overviewUri_queue, _bureauEnergyKeywordUrlPair, headers,dirRoute,objectiveFolder, objective,))
        overviewUriDistributor_proc.daemon = True
        overviewUriDistributor_proc.start()
        print(f'建立第{x}個 overviewUriDistributor_proc, {os.getpid()}, {overviewUriDistributor_proc}')
        Process_1.append(overviewUriDistributor_proc)


    Process_2 = []   # 爬overview html
    for p in range(30):
        getPageInARow_proc = mp.Process(target=getPageInARow, args=(overviewUri_queue, headers, objectiveFolder, objective,))
        getPageInARow_proc.daemon = True  #共同行程
        getPageInARow_proc.start()
        print(f'建立第{p}個 getPageInARow_proc, {os.getpid()}, {getPageInARow_proc}')
        Process_2.append(getPageInARow_proc)

    # 主行程
    # main process <--join--> overviewUriDistributor_proc ; overviewUriDistributor_proc <--join--> getPageInARow_proc
    distributeKeyword(_bureauEnergyKeywordUrlPair, keyword_queue)
    print("=============main process distributeKeyword 已經完成任務了。=============")


    #通知main process 完成事情。
    keyword_queue.join() 
    overviewUri_queue.join()

    print('Multiprocessing has done all jobs!')
    
    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')
    
    for proc in Process_2:
        proc.terminate()
        print(f'{proc} has terminated!')
    
    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))
