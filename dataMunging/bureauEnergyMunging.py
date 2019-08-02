# -*- coding:utf-8 -*-

"""
程式名稱：以『關鍵搜索字』爬蟲 經濟部能源局（經濟部能源局節能標章）。
程式描述：


https://www.energylabel.org.tw/





* detail的產品型號要同overview一樣清洗。

12個完成！完成！一共耗時：291.0394244194031 秒 總數量 : 0
"""


import json
# from bs4 import BeautifulSoup
# import time
import sys
import os
import multiprocessing as mp
_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH)   # 因為此行生效，所以才能引用他處的module


from libs.time import timeStampGenerator
from libs.time import timeCalculate
from libs.time import timeSleepOne
from libs.multiProcessing import distributeKeyword
from libs.multiProcessing import _bureauEnergyKeywordUrlPair
from libs.munging import bureauEnergyMunging
from libs.manipulateDir import mkdirForCleanData


# 清洗除濕機＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# detailJson檔案中，一加進overviewJson檔案的欄位。
def zipJsonObject(modelPoolDict, comparedValue, bureauEnergyDetail):
    # index = modelPool.index(comparedValue)
    # KeyError: 'HO-K85H'  'CU-M130HA2'#冷氣
    try:
        index = modelPoolDict[comparedValue]
        test_report_of_energy_efficiency = bureauEnergyDetail['productDetail'][index]['test_report_of_energy_efficiency']
        benchmark = bureauEnergyDetail['productDetail'][index]['efficiency_benchmark']
        annual = bureauEnergyDetail['productDetail'][index]['annual_power_consumption_degrees_dive_year']
        labelUri = bureauEnergyDetail['productDetail'][index]['energy_efficiency_label_innerUri']
    except KeyError as e:
        print(e)
        index, test_report_of_energy_efficiency, benchmark, annual, labelUri = 999999, "KeyError", "KeyError", "KeyError", "KeyError"
    return index, test_report_of_energy_efficiency, benchmark, annual, labelUri



def dataMunging(input, dirRoute, objectiveFolderClean, objective):
    # begin = timeCalculate()
    thisPID = os.getpid()
    while True:
        print(thisPID,"===========================================")
        searchword = input.get()

        dirNameCheck = dirRoute + f"{searchword}/"
        directory = dirRoute + f"{searchword}/detail/"
        dirNameWriteOut = dirRoute + f"{searchword}/jsonIntegration/"

        print('dataMunging is in new process %s, %s ' % (dataMunging_proc, thisPID))
        print()
        print('------接下來要處理資料夾路徑「 ' + dirNameWriteOut  + '」---------')
        print()


        mkdirForCleanData(objectiveFolderClean, objective)

        if not os.listdir(dirNameCheck):
            print(f"============={objective} {searchword} 資料夾沒有東西，此進程準備結束。=============")
            input.task_done()
            timeSleepOne()
            print("========================break========================")
            break

        # 此區已經採用簡化的寫法，因此若洗資料都無問題，那麼就可以刪除了。
        # if searchword == "除濕機":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailDehumidification(searchword, directory)
        # elif searchword == "無風管空氣調節機":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailAirConditioner(searchword, directory)
        # elif searchword == "電冰箱":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailRefrigerator(searchword, directory)
        # elif searchword == "電熱水瓶":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailElectricWarmer(searchword, directory)
        # elif searchword == "溫熱型開飲機":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailWarmDrinkMachine(searchword, directory)
        # elif searchword == "溫熱型飲水機":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailWarmDispenser(searchword, directory)
        # elif searchword == "冰溫熱型開飲機":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailColdWarmDrinkMachine(searchword, directory)
        # elif searchword == "冰溫熱型飲水機":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailColdWarmDispenser(searchword, directory)
        # elif searchword == "貯備型電熱水器":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailStorageWaterHeaters(searchword, directory)
        # elif searchword == "瓦斯熱水器":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailGasWaterHeaters(searchword, directory)
        # elif searchword == "瓦斯爐":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailGasStove(searchword, directory)
        # elif searchword == "安定器內藏式螢光燈泡":
        #     bureauEnergyDetail, totalNums = bureauMunging.detailCompactFluorescentLamp(searchword, directory)

        # '無風管空氣調節機', '除濕機', '電冰箱', '電熱水瓶', '溫熱型開飲機',
        # '溫熱型飲水機', '冰溫熱型開飲機', '冰溫熱型飲水機', '貯備型電熱水器' , '瓦斯熱水器', '瓦斯爐', '安定器內藏式螢光燈泡'
        bureauEnergyDetail, totalNums = bureauMunging.detailMungingEntry(searchword, directory)

        with open(dirNameWriteOut + f"{objective}_detail_{timeStampGenerator()}_{totalNums}_{searchword}.json",'w',encoding='utf-8')as f:
            json.dump(bureauEnergyDetail, f, indent=2, ensure_ascii=False)

        # 找出 overviewJsonFile ，開始與detailJsonFile合併：
        overviewJsonFile = [overviewFile for overviewFile in os.listdir(dirNameWriteOut) if "bureauEnergy_overview" in overviewFile].pop()
        with open(dirNameWriteOut + overviewJsonFile)as f:
            bureauEnergyOverview = json.load(f)

        modelPool = [comparedValue['product_model'] for comparedValue in bureauEnergyDetail['productDetail']]
        modelPoolDict = { v: k  for k, v in enumerate(modelPool)}


        #打開overviewJson檔案，為每個產品增加欄位。  
        for jsonObject in bureauEnergyOverview['product']:
            index, test_report_of_energy_efficiency, benchmark, annual, labelUri = zipJsonObject(modelPoolDict, jsonObject['product_model'], bureauEnergyDetail)
            
            # print('正在處理索引值： '+str(index))
            jsonObject['test_report_of_energy_efficiency'] = test_report_of_energy_efficiency
            jsonObject['efficiency_benchmark'] = benchmark
            jsonObject['annual_power_consumption_degrees_dive_year'] = annual
            jsonObject['energy_efficiency_label_innerUri'] = labelUri
            # print('done '+str(index))

        # 新增欄位的Json檔案更新時間。
        timeStamp = timeStampGenerator()
        bureauEnergyOverview["dateTime"] = timeStamp
        
        with open(f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}/{objective}_{timeStamp}_{totalNums}_{searchword}.json",'w',encoding='utf-8')as f:
            json.dump(bureauEnergyOverview, f, indent=2, ensure_ascii=False)

        statistic.append(totalNums)

        print(f"這裡是dataMunging_{thisPID}，準備完成工作。 ")
        print()
        end = timeCalculate()
        print('dataMunging 累計耗時：{0} 秒'.format(end-begin))
        input.task_done()  #通知main process此次的input處理完成！
        timeSleepOne() #暫停幾秒來模擬現實狀況。


if __name__ == '__main__':

    objectiveFolder = "rawData"

    objectiveFolderClean = "cleanData"

    objective = "bureauEnergy"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/"

    # dirRouteClean = f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}/"
    bureauMunging = bureauEnergyMunging()

    statistic = []

    begin = timeCalculate()

    #共同佇列
    keyword_queue = mp.JoinableQueue() # 發出關鍵字，讓接收的進程清洗該關鍵字的detail資料夾，同時合併detail and overview file。
    # airConditioner_queue = mp.JoinableQueue()


    # 啟動進程
    Process_1 = []  # 將overview資料夾的html打開清洗，並發送detailUri。
    for w in range(8):
        dataMunging_proc = mp.Process(target=dataMunging, args=(keyword_queue, dirRoute, objectiveFolderClean, objective,))
        dataMunging_proc.daemon = True
        dataMunging_proc.start()
        print(f'建立第{w}個 dataMunging_proc, {os.getpid()}, {dataMunging_proc}')
        Process_1.append(dataMunging_proc)

    # 主行程
    # main process <--join--> dataMunging_proc 
    distributeKeyword(_bureauEnergyKeywordUrlPair, keyword_queue)
    print("=============main process distributeKeyword 已經完成任務了。=============")

    #通知main process 完成事情。   # 開超過兩個queue，main process程式就無法跑通喔！
    keyword_queue.join() 
    

    print('Multiprocessing has done all jobs!')
    
    for proc in Process_1:
        proc.terminate()
        print(f'{proc} has terminated!')

    end = timeCalculate()
    
    TOTAL = sum(statistic)
    print('完成！一共耗時：{0} 秒'.format(end-begin), f'總數量 : {TOTAL}')
