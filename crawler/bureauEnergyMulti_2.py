# -*- coding:utf-8 -*-

"""
程式名稱：bureauEnergyMulti_2.py

程式描述：

    1. 以『關鍵分類搜索字』清洗爬蟲 經濟部能源局 的結果；再針對overview裡面的detailUrl進行詳細規格的爬蟲。

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
        * overview的產品型號要進行「源頭」清洗，將
        「\n」
        「" "」
        「非產品型號相關的 :UW-999(220V)、QB R 80 V 2,5K TW、LP-CH-910A(220V)附RO逆滲透純水機」
        等等都洗乾淨


    2. 

    input: _bureauEnergyKeywordUrlPair 的資訊。

    Output: 1. 將每個類別overview的 html，清洗好後存成json。
            2. 再將每個分類json裡面的detailUrl拿出來爬蟲，以txt形式儲存本地。
            3. 見/dataMunging/bureauEnergy/關鍵字/detail/  or /dataMunging/bureauEnergy/關鍵字/jsonIntegration/。
            
            

備　　註：


30個進程，


備　　註：
5076 ===========================================
這裡是 detailPageInARow 完成: 8054_8055_無風管空氣調節機.txt 的爬取。
detailPageInARow 累計耗時：6977.335040330887 秒
5048 ===========================================
這裡是 detailPageInARow 完成: 8052_8055_無風管空氣調節機.txt 的爬取。
detailPageInARow 累計耗時：6978.0827560424805 秒
5073 ===========================================
這裡是 detailPageInARow 完成: 8051_8055_無風管空氣調節機.txt 的爬取。
detailPageInARow 累計耗時：6978.326544046402 秒
5071 ===========================================



"""


from bs4 import BeautifulSoup
import requests
# import time
import os
import sys
# import random
import json
import multiprocessing as mp
from urllib.parse import urlparse, parse_qs

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)

from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.manipulateDir import initialFile
from libs.multiProcessing import distributeKeyword
from libs.multiProcessing import _bureauEnergyKeywordUrlPair
from libs.time import timeSleepRandomly
from libs.time import timeSleepTwo
from libs.time import timeSleepOne
from libs.time import timeStampGenerator
from libs.time import timeCalculate
from libs.regex import bureauEnergyReplace
from libs.regex import discardSpace
from libs.requests import _headers




def dataMunging(input, output, dirRoute,objectiveFolder, objective, domainUrl, *args):
    begin = timeCalculate()
    thisPID = os.getpid()
    energyLabelUrl = "https://ranking.energylabel.org.tw/_Upload/applyMain/applyp/"
    while True:
        print(thisPID,"===========================================")
        searchword = input.get() 
        dirNameAccepted = dirRoute + f"{searchword}/overview/"
        dirNameWriteOut = dirRoute + f"{searchword}/"

        #莫把檢查資料夾的工作放到爬蟲時才做，那樣會對資料夾開開刪刪。
        eraseRawData(objectiveFolder, objective, searchword, keyword="jsonIntegration")
        mkdirForRawData(objectiveFolder, objective, searchword, keyword="jsonIntegration")

        print('dataMunging is in new process %s, %s ' % (dataMunging_proc, thisPID))
        print()
        print('------接下來要處理資料夾路徑「 ' + dirNameAccepted + '」---------')
        print()
        
        if not os.listdir(dirNameAccepted):
            print(f"============={objective} {searchword} 資料夾沒有東西，此進程準備結束。=============")
            input.task_done()
            timeSleepOne()
            print("========================break========================")
            break

        bureauEnergyDict = {}
        productArray= [] 
        
        for file in initialFile(dirNameAccepted):
            # print(" start " + file + " ! ")
                
            with open(dirNameAccepted + file)as f:
                inn = f.read()
            textSoup = BeautifulSoup(inn,'html.parser')

            a = 0
            b = 7

            for i in range(10): #每頁有十項，每7個元素一組
                oneset = textSoup.find_all('div',{'class':'col-md-12 column'})[-1].find_all('td',{'align':'left'})[a:b]
                if oneset != []:
                    
                    detailUrl =  domainUrl + oneset[2].a.attrs.get('href')
                    
                    parseUrl = urlparse(detailUrl)
                    qsDict = parse_qs(parseUrl.query)
                    p1 = qsDict['id'].pop() #id是p1
                    p0 = qsDict['p0'].pop()
                    
                    productDict = {}
                    productDict['Id'] = p1 #oneset[2].a.attrs.get('href').split('id=')[1]
                    #  檔案裡面有髒值  冰箱"product_model": "B23KV-81RE\n", "IB 7030 F TW"     空調"product_model": "PAX-K500CLD ",
                    productDict['product_model'] = bureauReplace.productModel(oneset[0].text)
                    productDict['brand_name'] = oneset[1].text
                    productDict['login_number'] = oneset[2].text
                    productDict['detailUri'] = detailUrl
                    productDict['labeling_company'] = oneset[3].text
                    productDict['efficiency_rating'] = oneset[4].text
                    productDict['from_date_of_expiration'] = bureauReplace.date(oneset[5].text)
                    
                    # 我們可以組裝outerUri
                    # https://ranking.energylabel.org.tw/product/Approval/file_list.aspx?p1=20901&p0=82409
                    productDict['energy_efficiency_label_outerUri'] = f"{domainUrl}file_list.aspx?p1={p1}&p0={p0}"
                    
                    # 我們想要的InnerUri
                    # https://ranking.energylabel.org.tw/_Upload/applyMain/applyp/20901/SB_photo1/EF2R-13DEX1.jpg
                    # productDict['energy_efficiency_label_innerUri'] = ... 因為這邊要做判斷，因此在 「bureauEnergyMunging.py」再處理，以不影響爬蟲的進度。


                    productArray.append(productDict)

                    a += 7
                    b += 7
                    # print('done ' + file + ' 的第' + str(i+1) + '份。')
                else:
                    print('在 ' + file + ' 的第' + str(i+1) + '處，發現空值！')
                    break
            
        bureauEnergyDict['product'] = productArray
        bureauEnergyDict['keyword'] = searchword
        timeStamp = timeStampGenerator()
        bureauEnergyDict["dateTime"] = timeStamp

        totalNums = len(bureauEnergyDict['product'])
        
        with open(dirNameWriteOut + f"jsonIntegration/{objective}_overview_{timeStamp}_{totalNums}_{searchword}.json","w",encoding="utf-8")as f:
            json.dump(bureauEnergyDict, f, indent=2, ensure_ascii=False)
        
        print(f'這裡是 dataMunging ，處理{searchword}完成: ' + dirNameWriteOut + "jsonIntegration/")


        # ＝＝＝＝＝＝＝＝＝ 如果只想要洗 overview html，此區可以註解掉。＝＝＝＝＝＝＝＝＝＝
        # 莫把檢查資料夾的工作放到爬蟲時才做，那樣會對資料夾開開刪刪。
        eraseRawData(objectiveFolder, objective, searchword, keyword="detail")
        mkdirForRawData(objectiveFolder, objective, searchword, keyword="detail")
        
        productIndex = 1
        for file in bureauEnergyDict['product']:
            detailUri = file['detailUri']
            readyTxtFileRoute = dirNameWriteOut + f"detail/{productIndex}_{totalNums}_{searchword}.txt"
            
            #TypeError: must be str, not tuple
            consecutiveData = searchword + "+" + detailUri + "+" + readyTxtFileRoute

            output.put(consecutiveData)
            # print('這裡是 dataMunging，準備送給  detailPageInARow  處理: ' + consecutiveData)
            # print()            
            productIndex += 1
        # ＝＝＝＝＝＝＝＝＝ ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝



        end = timeCalculate()
        print('dataMunging 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()
        timeSleepOne() #暫停幾秒來模擬現實狀況。



def detailPageInARow(input,  headers, objectiveFolder, objective, *args):
    begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        
        consecutiveUrl = input.get()
        searchword, url, txtFileRoute = consecutiveUrl.split("+")
        # searchword = consecutiveUrl.split("+")[0]
        # url = consecutiveUrl.split("+")[1]
        # txtFileRoute = consecutiveUrl.split("+")[2]
        
        print('detailPageInARow is in new process %s, %s ' % (detailPageInARow_proc, thisPID))
        print()
        
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'

        timeSleepRandomly()

        soup  = BeautifulSoup(res.text,'html.parser')

        with open(txtFileRoute, 'w', encoding='utf-8')as f:
            f.write(str(soup))
        
        fileName = txtFileRoute.split("/")[-1]
        productIndex = fileName.split("_")[0]
        productNums = fileName.split("_")[1]
        print(f"成功寫出  {searchword}  detail頁， 第 {productIndex} 項， 共 {productNums} 項。")
            
        timeSleepRandomly()
        timeSleepOne()

        print('這裡是 detailPageInARow 完成: ' + fileName + " 的爬取。")
        end = timeCalculate()
        print('detailPageInARow 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()
        


if __name__ == '__main__':
    
    headers = _headers

    begin = timeCalculate()

    objectiveFolder = "rawData"

    # objectiveFolderClean = "cleanData"

    objective = "bureauEnergy"
    
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/"
    
    domainUrl = 'https://ranking.energylabel.org.tw/product/Approval/'

    bureauReplace = bureauEnergyReplace()
    
    print('-------------------------------------------------------------------------')

    #共同佇列
    keyword_queue = mp.JoinableQueue() # 發出關鍵字，讓接收的進程清洗該關鍵字的overview資料夾。
    detailUri_queue = mp.JoinableQueue() #接收detailUri後爬取詳細規格html

    # 啟動進程
    Process_1 = []  # 將overview資料夾的html打開清洗，並發送detailUri。  有12個分類
    for w in range(8):
        dataMunging_proc = mp.Process(target=dataMunging, args=(keyword_queue, detailUri_queue, dirRoute,objectiveFolder, objective, domainUrl,))
        dataMunging_proc.daemon = True
        dataMunging_proc.start()
        print(f'建立第{w}個 dataMunging_proc, {os.getpid()}, {dataMunging_proc}')
        Process_1.append(dataMunging_proc)


    Process_2 = [] # 接收detailUri，繼續爬蟲html。
    for k in range(40):
        detailPageInARow_proc = mp.Process(target=detailPageInARow, args=(detailUri_queue, headers, objectiveFolder, objective,))
        detailPageInARow_proc.daemon = True
        detailPageInARow_proc.start()
        print(f'建立第{k}個 detailPageInARow_proc, {os.getpid()}, {detailPageInARow_proc}')
        Process_2.append(detailPageInARow_proc)


    # 主行程
    # main process <--join--> dataMunging_proc ; dataMunging_proc <--join-->  detailUriDitributor_proc  
    distributeKeyword(_bureauEnergyKeywordUrlPair, keyword_queue)
    print("=============main process distributeKeyword 已經完成任務了。=============")


    #通知main process 完成事情。   # 開超過兩個queue，main process程式就無法跑通喔！
    keyword_queue.join() 
    detailUri_queue.join()
    


    print('Multiprocessing has done all jobs!')
    
    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')
    
    for proc in Process_2:
        proc.terminate()
        print(f'{proc} has terminated!')

    
    end = timeCalculate()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))
