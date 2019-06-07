# -*- coding:utf-8 -*-

"""
程式名稱：以『關鍵搜索字』爬蟲 經濟部能源局（經濟部能源局節能標章）。
程式描述：


https://www.energylabel.org.tw/


    

備　　註：


50個進程，完成！一共耗時：1236.2417197227478 秒


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
sys.path.append(_BASE_PATH)

from libs.manipulateDir import mkdirForRawData
from libs.manipulateDir import eraseRawData
from libs.manipulateDir import initialFile
from libs.multiProcessing import distributeKeyword
from libs.time import timeSleepRandomly
from libs.time import timeSleepTwo
from libs.time import timeSleepOne
from libs.time import timeStampGenerator


def dataMunging(input, output, dirRoute,objectiveFolder, objective, domainUrl, *args):
    begin = time.time()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        searchword = input.get() 
        dirNameAccepted = dirRoute + f"{searchword}/overview/"
        dirNameWriteOut = dirRoute + f"{searchword}/"

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
            print(" start " + file + " ! ")
                
            with open(dirNameAccepted + file)as f:
                inn = f.read()
            textSoup = BeautifulSoup(inn,'html.parser')

            a = 0
            b = 7

            for i in range(10): #每頁有十項，每7個元素一組
                oneset = textSoup.find_all('div',{'class':'col-md-12 column'})[-1].find_all('td',{'align':'left'})[a:b]
                if oneset != []:

                    productDict = {}
                    productDict['Id'] = oneset[2].a.attrs.get('href').split('id=')[1]
                    #  檔案裡面有髒值  冰箱"product_model": "B23KV-81RE\n", "IB 7030 F TW"     空調"product_model": "PAX-K500CLD ",
                    productDict['product_model'] = oneset[0].text.replace("\n","").replace(" ","")
                    productDict['brand_name'] = oneset[1].text
                    productDict['login_number'] = oneset[2].text
                    productDict['detailUri'] = domainUrl + oneset[2].a.attrs.get('href')
                    productDict['labeling_company'] = oneset[3].text
                    productDict['efficiency_rating'] = oneset[4].text
                    productDict['from_date_of_expiration'] = oneset[5].text.replace('/','-')
                    productArray.append(productDict)

                    a += 7
                    b += 7
                    print('done ' + file + ' 的第' + str(i+1) + '份。')
                else:
                    print('在 ' + file + ' 的第' + str(i+1) + '處，發現空值！')
                    break
            
        bureauEnergyDict['product'] = productArray
        bureauEnergyDict['keyword'] = searchword
        bureauEnergyDict["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDict['product'])
        
        with open(dirNameWriteOut + f"{objective}_overview_{totalNums}_{searchword}.json","w",encoding="utf-8")as f:
            json.dump(bureauEnergyDict, f, indent=2, ensure_ascii=False)
        
        print(f'這裡是 dataMunging ，處理{searchword}完成: ' + dirNameWriteOut)


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
            print('這裡是 dataMunging，準備送給  detailPageInARow  處理: ' + consecutiveData)
            print()            
            productIndex += 1
        # ＝＝＝＝＝＝＝＝＝ ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝



        end = time.time()
        print('dataMunging 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()
        timeSleepOne() #暫停幾秒來模擬現實狀況。



def detailPageInARow(input,  headers, objectiveFolder, objective, *args):
    begin = time.time()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        
        consecutiveUrl = input.get()

        searchword = consecutiveUrl.split("+")[0]
        url = consecutiveUrl.split("+")[1]
        txtFileRoute = consecutiveUrl.split("+")[2]
        
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

        print('這裡是 detailPageInARow 完成: ' + fileName + " 的爬取。")
        end = time.time()
        print('detailPageInARow 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()
        


if __name__ == '__main__':
    

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
          "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4","Connection":"close"}
    
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
    
    domainUrl = 'https://ranking.energylabel.org.tw/product/Approval/'

    print('-------------------------------------------------------------------------')

    #共同佇列
    keyword_queue = mp.JoinableQueue() # 發出關鍵字，讓接收的進程清洗該關鍵字的overview資料夾。
    detailUri_queue = mp.JoinableQueue() #接收detailUri後爬取詳細規格html

    # 啟動進程
    Process_1 = []  # 將overview資料夾的html打開清洗，並發送detailUri。
    for w in range(8):
        dataMunging_proc = mp.Process(target=dataMunging, args=(keyword_queue, detailUri_queue, dirRoute,objectiveFolder, objective, domainUrl,))
        dataMunging_proc.daemon = True
        dataMunging_proc.start()
        print(f'建立第{w}個 dataMunging_proc, {os.getpid()}, {dataMunging_proc}')
        Process_1.append(dataMunging_proc)


    Process_2 = [] # 接收detailUri，繼續爬蟲html。
    for k in range(50):
        detailPageInARow_proc = mp.Process(target=detailPageInARow, args=(detailUri_queue, headers, objectiveFolder, objective,))
        detailPageInARow_proc.daemon = True
        detailPageInARow_proc.start()
        print(f'建立第{k}個 detailPageInARow_proc, {os.getpid()}, {detailPageInARow_proc}')
        Process_2.append(detailPageInARow_proc)


    # 主行程
    # main process <--join--> dataMunging_proc ; dataMunging_proc <--join-->  detailUriDitributor_proc  
    distributeKeyword(keywordUrlPair, keyword_queue)
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

    
    end = time.time()
    
    print('完成！一共耗時：{0} 秒'.format(end-begin))
