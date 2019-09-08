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

成功寫出  無風管空氣調節機  detail頁， 第 2541 項， 共 8055 項。
7836 ===========================================
成功寫出  瓦斯熱水器  detail頁， 第 2609 項， 共 5395 項。
成功寫出  瓦斯熱水器  detail頁， 第 2610 項， 共 5395 項。
成功寫出  瓦斯爐  detail頁， 第 2582 項， 共 7740 項。
成功寫出  瓦斯爐  detail頁， 第 2583 項， 共 7740 項。
成功寫出  無風管空氣調節機  detail頁， 第 2543 項， 共 8055 項。
成功寫出  瓦斯爐  detail頁， 第 2584 項， 共 7740 項。
7837 ===========================================
7855 ===========================================
7854 ===========================================
成功寫出  瓦斯熱水器  detail頁， 第 2611 項， 共 5395 項。
成功寫出  無風管空氣調節機  detail頁， 第 2544 項， 共 8055 項。
7843 ===========================================
7857 ===========================================
7839 ===========================================
成功寫出  瓦斯爐  detail頁， 第 2586 項， 共 7740 項。
成功寫出  瓦斯熱水器  detail頁， 第 2612 項， 共 5395 項。
7833 ===========================================
7852 ===========================================
成功寫出  瓦斯熱水器  detail頁， 第 2613 項， 共 5395 項。
成功寫出  瓦斯爐  detail頁， 第 2585 項， 共 7740 項。
成功寫出  無風管空氣調節機  detail頁， 第 2545 項， 共 8055 項。
7851 ===========================================
7842 ===========================================
成功寫出  瓦斯爐  detail頁， 第 2587 項， 共 7740 項。
7841 ===========================================

https://docs.python.org/3/library/socket.html
https://www.programcreek.com/python/example/528/socket.gaierror
https://kite.com/python/docs/socket.gaierror
根據文件，這個似乎是dns暫時異常導致的問題！


Process Process-40:
Traceback (most recent call last):
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/connection.py", line 160, in _new_conn
    (self._dns_host, self.port), self.timeout, **extra_kw)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/util/connection.py", line 57, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "/home/bluevc/.pyenv/versions/3.6.8/lib/python3.6/socket.py", line 745, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno -3] Temporary failure in name resolution

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/connectionpool.py", line 603, in urlopen
    chunked=chunked)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/connectionpool.py", line 344, in _make_request
    self._validate_conn(conn)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/connectionpool.py", line 843, in _validate_conn
    conn.connect()
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/connection.py", line 316, in connect
    conn = self._new_conn()
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/connection.py", line 169, in _new_conn
    self, "Failed to establish a new connection: %s" % e)
urllib3.exceptions.NewConnectionError: <urllib3.connection.VerifiedHTTPSConnection object at 0x7ffbd2c33a90>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/requests/adapters.py", line 449, in send
    timeout=timeout
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/connectionpool.py", line 641, in urlopen
    _stacktrace=sys.exc_info()[2])
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/urllib3/util/retry.py", line 399, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='ranking.energylabel.org.tw', port=443): Max retries exceeded with url: /product/Approval/upt.aspx?pageno=254&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=49&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&p0=73944&id=18579 (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7ffbd2c33a90>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution',))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/bluevc/.pyenv/versions/3.6.8/lib/python3.6/multiprocessing/process.py", line 258, in _bootstrap
    self.run()
  File "/home/bluevc/.pyenv/versions/3.6.8/lib/python3.6/multiprocessing/process.py", line 93, in run
    self._target(*self._args, **self._kwargs)
  File "/home/bluevc/2019/iSelect3C/crawler/bureauEnergyMulti_2.py", line 230, in detailPageInARow
    res = requests.get(url, headers=headers)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/requests/api.py", line 75, in get
    return request('get', url, params=params, **kwargs)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/requests/api.py", line 60, in request
    return session.request(method=method, url=url, **kwargs)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/requests/sessions.py", line 533, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/requests/sessions.py", line 646, in send
    r = adapter.send(request, **kwargs)
  File "/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='ranking.energylabel.org.tw', port=443): Max retries exceeded with url: /product/Approval/upt.aspx?pageno=254&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=49&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&p0=73944&id=18579 (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7ffbd2c33a90>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution',))



40 個進程：完成！一共耗時：5538.415146112442 秒

20 個 完成！一共耗時：11191.768384218216 秒

30 個 完成！一共耗時：7815.017035245895 秒


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
# from socket import gaierror
import socket

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)

from libs.manipulateDir import (
                              mkdirForRawData,
                              eraseRawData,
                              initialFileZeroUnderscoreInt
                              )
from libs.multiProcessing import (
                              distributeKeyword,
                              _bureauEnergyKeywordUrlPair
                              )
from libs.timeWidget import (
                          timeSleepRandomly,
                          timeSleepTwo,
                          timeSleepOne,
                          timeStampGenerator,
                          timeCalculate
                          )
from libs.regex import (
                    bureauEnergyReplace,
                    discardSpace
                    )
from libs.httpRequests import _headers




def dataMunging(input, output, dirRoute,objectiveFolder, objective, domainUrl, *args):
    thisPID = os.getpid()
    energyLabelUrl = "https://ranking.energylabel.org.tw/_Upload/applyMain/applyp/"
    bureauReplace = bureauEnergyReplace()
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
        
        for file in initialFileZeroUnderscoreInt(dirNameAccepted):
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



def badRequestComposed(searchword, url, txtFileRoute):
  fileName = txtFileRoute.split("/")[-1]
  badRequestRoute = "/".join(txtFileRoute.split("/")[:-3]) + "/badRequest"
  with open(f"{badRequestRoute}/badRequest_{searchword}.txt", "a",  newline='', encoding='utf-8')as f: # newline沒作用...
      errorMessage = url + "＋" + f"「{fileName}」" +"\n"
      f.write(errorMessage)   #writelines作用在errorMessage是list時

def judgeSoup(soup, searchword, url, txtFileRoute):
  if not soup:
    badRequestComposed(searchword, url, txtFileRoute)
  elif soup.select_one('head').text.strip() == 'Service Unavailable':
    """

    「
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN""http://www.w3.org/TR/html4/strict.dtd">

    <html><head><title>Service Unavailable</title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/></head>
    <body><h2>Service Unavailable</h2>
    <hr/><p>HTTP Error 503. The service is unavailable.</p>
    </body></html>
    」

    """
    soup = ""
    badRequestComposed(searchword, url, txtFileRoute)
  else:
    pass

def detailPageInARow(input,  headers, objectiveFolder, objective, *args):
    """
    As many as 28,000 detail urls we are supposed to crawl would inevitalby leave some processes to fail to get the correct responses.
    As such, we should extend more time while crawling , or establish exception handler in porgrams.
    
    """
    # begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        # print(thisPID,"===========================================")
        
        consecutiveUrl = input.get()
        searchword, url, txtFileRoute = consecutiveUrl.split("+")
        
        # print('detailPageInARow is in new process %s, %s ' % (detailPageInARow_proc, thisPID))
        # print()

        for i in range(3):
            try:
              timeSleepTwo()
              res = requests.get(url, headers=headers)
              res.encoding = 'utf-8'
              timeSleepRandomly()
              soup  = BeautifulSoup(res.text,'html.parser')
              break
            except requests.exceptions.ConnectionError as e:
              print(url, "發生問題。", e)
              print()
              timeSleepRandomly()
              timeSleepTwo()
              timeSleepTwo()
              soup = ""
        
        judgeSoup(soup, searchword, url, txtFileRoute)
        


        with open(txtFileRoute, 'w', encoding='utf-8')as f:
            f.write(str(soup))
        
        fileName = txtFileRoute.split("/")[-1]
        productIndex = fileName.split("_")[0]
        productNums = fileName.split("_")[1]
        print(f"{thisPID}__成功寫出  {searchword}  detail頁， 第 {productIndex} 項， 共 {productNums} 項。")
            
        timeSleepRandomly()

        # print('這裡是 detailPageInARow 完成: ' + fileName + " 的爬取。")
        end = timeCalculate()
        # print('detailPageInARow 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()
        


if __name__ == '__main__':
    
    headers = _headers

    begin = timeCalculate()

    objectiveFolder = "rawData"

    # objectiveFolderClean = "cleanData"

    objective = "bureauEnergy"
    
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/"
    
    domainUrl = 'https://ranking.energylabel.org.tw/product/Approval/'

    eraseRawData(objectiveFolder, objective, "badRequest")
    mkdirForRawData(objectiveFolder, objective, "badRequest")
    
    print('-------------------------------------------------------------------------')

    #共同佇列
    keyword_queue = mp.JoinableQueue() # 發出關鍵字，讓接收的進程清洗該關鍵字的overview資料夾。
    detailUri_queue = mp.JoinableQueue() #接收detailUri後爬取詳細規格html

    # 啟動進程
    Process_1 = []  # 將overview資料夾的html打開清洗，並發送detailUri。  有12個分類
    for w in range(3):
        dataMunging_proc = mp.Process(target=dataMunging, args=(keyword_queue, detailUri_queue, dirRoute,objectiveFolder, objective, domainUrl,))
        dataMunging_proc.daemon = True
        dataMunging_proc.start()
        print(f'建立第{w}個 dataMunging_proc, {os.getpid()}, {dataMunging_proc}')
        Process_1.append(dataMunging_proc)


    Process_2 = [] # 接收detailUri，繼續爬蟲html。
    for k in range(30):
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
