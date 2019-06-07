# -*- coding:utf-8 -*-

"""
程式名稱：以『關鍵搜索字』爬蟲 經濟部能源局（經濟部能源局節能標章）。
程式描述：


https://www.energylabel.org.tw/


30個進程，完成！一共耗時：211.93192338943481 秒

備　　註：



"""


from bs4 import BeautifulSoup
import requests
import time
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
from libs.time import timeSleepRandomly
from libs.time import timeSleepOne



def overviewUriDistributor(input, output, keywordUrlPair, headers, dirRoute,objectiveFolder, objective, *args):
    begin = time.time()
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
            
        end = time.time()
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
    begin = time.time()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        consecutiveUrl = input.get()
        searchword = consecutiveUrl.split("+")[0]
        correctUrl = consecutiveUrl.split("+")[1]
        txtFileRoute = consecutiveUrl.split("+")[2]
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
        end = time.time()
        print('getPageInARow 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()  #通知main process此次的input處理完成！
        timeSleepOne() #暫停幾秒來模擬現實狀況。


if __name__ == '__main__':
    

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
          "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4","Connection":"close"}
    

    # urlDehumidifier   urlRefri   urlElectricThermos
    keywordUrlPair = {"無風管空氣調節機":("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=49"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "除濕機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=55"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "電冰箱" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=56"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "電熱水瓶" :  ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=47"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "溫熱型開飲機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=50"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "溫熱型飲水機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=53"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "冰溫熱型開飲機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=52"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "冰溫熱型飲水機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=54"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno=")
                                }    
    begin = time.time()

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
    Process_1 = []  #發送overviewUri
    for x in range(8):
        overviewUriDistributor_proc = mp.Process(target=overviewUriDistributor, args=(keyword_queue, overviewUri_queue, keywordUrlPair, headers,dirRoute,objectiveFolder, objective,))
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
    distributeKeyword(keywordUrlPair, keyword_queue)
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
    
    end = time.time()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))
