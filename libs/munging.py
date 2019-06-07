# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os
import sys
from bs4 import BeautifulSoup
_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.time import timeSleepOne
from libs.time import timeStampGenerator
from libs.manipulateDir import initialFile
from libs.regex import interDiv
from libs.regex import searchFloatNums
# from libs.regex import searchNums
from libs.regex import floatDiv

def EcommerceDataProcessToSet(productList):
    productArray = [file for file in productList]

    print("未去重總筆數", len(productArray))
    setDict = {}
    for file in productArray:
        setDictInner = {}
        setDictInner['name'] = file['name']
        setDictInner['originprice'] = file['originprice']
        setDictInner['pics'] = file['pics']
        setDictInner['picb'] = file['picb']
        setDictInner['produrl'] = file['produrl']
        
        setDict[file['Id']] = setDictInner
    
    print("去重總比數", len(setDict))

    # 重新組裝
    rebuildArray = []
    for key in setDict:
        rebuildSetDict = {}
        rebuildSetDict['Id'] = key
        rebuildSetDict['name'] = setDict[key]['name']
        rebuildSetDict['originprice'] = setDict[key]['originprice']
        rebuildSetDict['pics'] = setDict[key]['pics']
        rebuildSetDict['picb'] = setDict[key]['picb']
        rebuildSetDict['produrl'] = setDict[key]['produrl']

        rebuildArray.append(rebuildSetDict)

    return rebuildArray, len(rebuildArray)



def selectColumn(textSoup, row):
    selected = textSoup.find('div',{'class':'row text-center col-sm-12'}).select('.row')[row].text
    selected = selected.split('：')[1]
    return selected


#  detail 檔案裡面有髒值  冰箱"product_model": "B23KV-81RE\n",   "IB 7030 F TW" 空調"product_model": "PAX-K500CLD ",

def mungingDetailDehumidification(searchword, directory): #除濕機
        bureauEnergyDetail = {}
        productDetailArray = []
        
        for file in initialFile(directory):
        #     print("start: " + file)
            with open(directory + file)as f:
                inn = f.read()
            productDetail = {}
            textSoup = BeautifulSoup(inn,'html.parser')

            productDetail['product_model'] = selectColumn(textSoup, 2).replace("\n","").replace(" ","")  #v
            productDetail["test_report_of_energy_efficiency"]  = {"rated_dehumidification_capacity": selectColumn(textSoup, 3).replace("公升/日", " L/day"), 
                                                                "energy_factor_value": selectColumn(textSoup, 4).replace("公升/千瓦小時公升", " L/kWh")}
            productDetail["efficiency_benchmark"] = selectColumn(textSoup, 6).replace("公升/千瓦小時", " L/kWh") #v
            productDetail["annual_power_consumption_degrees_dive_year"] = searchFloatNums(selectColumn(textSoup, 9))#V
            productDetailArray.append(productDetail)
            
        #     print('done: ' + file)
        
        bureauEnergyDetail['productDetail'] = productDetailArray
        bureauEnergyDetail['keyword'] = searchword
        bureauEnergyDetail["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDetail['productDetail'])

        return bureauEnergyDetail, totalNums



def mungingDetailAirConditioner(searchword, directory): #無風管空氣調節機
        bureauEnergyDetail = {}
        productDetailArray = []

        for file in initialFile(directory):
                # print('start: '+file)
                with open(directory + file)as f:
                        inn = f.read()
                productDetail = {}
                textSoup = BeautifulSoup(inn,'html.parser')

                productDetail['product_model'] = selectColumn(textSoup, 2).replace("\n","").replace(" ","") 
                productDetail["test_report_of_energy_efficiency"] = {"EER": str(floatDiv(selectColumn(textSoup, 4),selectColumn(textSoup, 6)))+' kW/kW', 
                                                                "CSPF": selectColumn(textSoup, 8)}
                productDetail["efficiency_benchmark"] = selectColumn(textSoup, 10)
                productDetail["annual_power_consumption_degrees_dive_year"] = searchFloatNums(selectColumn(textSoup, 13))
                productDetailArray.append(productDetail)

                print('done: '+file)
    
        bureauEnergyDetail['productDetail'] = productDetailArray
        bureauEnergyDetail['keyword'] = searchword
        bureauEnergyDetail["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDetail['productDetail'])

        return bureauEnergyDetail, totalNums

def mungingDetailRefrigerator(searchword, directory): # 電冰箱
        bureauEnergyDetail = {}
        productDetailArray = []
        
        for file in initialFile(directory):
                # print('start: '+file)
                with open(directory + file)as f:
                        inn = f.read()
                productDetail = {}
                textSoup = BeautifulSoup(inn,'html.parser')
                productDetail['product_model'] = selectColumn(textSoup, 2).replace("\n","").replace(" ","")  #v
                productDetail["test_report_of_energy_efficiency"]  = {"effective_internal_volume": selectColumn(textSoup, 3).replace("公升", " L"), 
                                                                        "energy_factor_value": selectColumn(textSoup, 4).replace("公升/度/月", " L/kWh/month")}
                productDetail["efficiency_benchmark"] = selectColumn(textSoup, 6).replace("公升/度/月", " L/kWh/month") #v
                productDetail["annual_power_consumption_degrees_dive_year"] = searchFloatNums(selectColumn(textSoup, 9))#V
                productDetailArray.append(productDetail)
                # print('done: '+file)
        
        bureauEnergyDetail['productDetail'] = productDetailArray
        bureauEnergyDetail['keyword'] = searchword
        bureauEnergyDetail["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDetail['productDetail'])

        return bureauEnergyDetail, totalNums


def mungingDetailElectricWarmer(searchword, directory): #電熱水瓶
        bureauEnergyDetail = {}
        productDetailArray = []
        
        for file in initialFile(directory):
                # print('start: '+file)
                with open(directory + file)as f:
                        inn = f.read()
                productDetail = {}
                textSoup = BeautifulSoup(inn,'html.parser')
                productDetail['product_model'] = selectColumn(textSoup, 2).replace("\n","").replace(" ","")  #v
                productDetail["test_report_of_energy_efficiency"]  = {"effective_internal_volume": selectColumn(textSoup, 3).replace("公升", " L"), 
                                                                        "est,24": selectColumn(textSoup, 4).replace("(kWh/24小時)", " kWh/24hr")}
                productDetail["efficiency_benchmark"] = selectColumn(textSoup, 6) #v
                productDetail["annual_power_consumption_degrees_dive_year"] = searchFloatNums(selectColumn(textSoup, 9))#V
                productDetailArray.append(productDetail)
                # print('done: '+file)
        
        bureauEnergyDetail['productDetail'] = productDetailArray
        bureauEnergyDetail['keyword'] = searchword
        bureauEnergyDetail["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDetail['productDetail'])

        return bureauEnergyDetail, totalNums



def mungingDetailWarmDrinkMachine(searchword, directory): #溫熱型開飲機
        bureauEnergyDetail = {}
        productDetailArray = []
        
        for file in initialFile(directory):
                # print('start: '+file)
                with open(directory + file)as f:
                        inn = f.read()
                productDetail = {}
                textSoup = BeautifulSoup(inn,'html.parser')
                productDetail['product_model'] = selectColumn(textSoup, 2).replace("\n","").replace(" ","")  #v
                productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": selectColumn(textSoup, 3).replace("公升", " L"), 
                                                                        "est,24": selectColumn(textSoup, 4).replace("(kWh/24小時)", " kWh/24hr")}
                productDetail["efficiency_benchmark"] = selectColumn(textSoup, 6) #v
                productDetail["annual_power_consumption_degrees_dive_year"] = searchFloatNums(selectColumn(textSoup, 9))#V
                productDetailArray.append(productDetail)
                # print('done: '+file)
        
        bureauEnergyDetail['productDetail'] = productDetailArray
        bureauEnergyDetail['keyword'] = searchword
        bureauEnergyDetail["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDetail['productDetail'])

        return bureauEnergyDetail, totalNums

def mungingDetailWarmDispenser(searchword, directory):#溫熱型飲水機
        bureauEnergyDetail = {}
        productDetailArray = []
        
        for file in initialFile(directory):
                # print('start: '+file)
                with open(directory + file)as f:
                        inn = f.read()
                productDetail = {}
                textSoup = BeautifulSoup(inn,'html.parser')
                productDetail['product_model'] = selectColumn(textSoup, 2).replace("\n","").replace(" ","")  #v
                productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": selectColumn(textSoup, 3).replace("公升", " L"), 
                                                                        "est,24": selectColumn(textSoup, 4).replace("(kWh/24小時)", " kWh/24hr")}
                productDetail["efficiency_benchmark"] = selectColumn(textSoup, 6) #v
                productDetail["annual_power_consumption_degrees_dive_year"] = searchFloatNums(selectColumn(textSoup, 9))#V
                productDetailArray.append(productDetail)
                # print('done: '+file)
        
        bureauEnergyDetail['productDetail'] = productDetailArray
        bureauEnergyDetail['keyword'] = searchword
        bureauEnergyDetail["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDetail['productDetail'])

        return bureauEnergyDetail, totalNums

def mungingDetailColdWarmDrinkMachine(searchword, directory): #冰溫熱型開飲機
        bureauEnergyDetail = {}
        productDetailArray = []
        
        for file in initialFile(directory):
                # print('start: '+file)
                with open(directory + file)as f:
                        inn = f.read()
                productDetail = {}
                textSoup = BeautifulSoup(inn,'html.parser')
                productDetail['product_model'] = selectColumn(textSoup, 2).replace("\n","").replace(" ","")  #v
                productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": selectColumn(textSoup, 3).replace("公升", " L"), 
                                                                        "warm_water_system_storage_tank_capacity_indication_value": selectColumn(textSoup, 4).replace("公升", " L").replace('\t',''),
                                                                        "est,24": selectColumn(textSoup, 5).replace("(kWh/24小時)", " kWh/24hr")}
                productDetail["efficiency_benchmark"] = selectColumn(textSoup, 7) #v
                productDetail["annual_power_consumption_degrees_dive_year"] = searchFloatNums(selectColumn(textSoup, 10))#V
                productDetailArray.append(productDetail)
                # print('done: '+file)
        
        bureauEnergyDetail['productDetail'] = productDetailArray
        bureauEnergyDetail['keyword'] = searchword
        bureauEnergyDetail["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDetail['productDetail'])

        return bureauEnergyDetail, totalNums

def mungingDetailColdWarmDispenser(searchword, directory): #冰溫熱型飲水機
        bureauEnergyDetail = {}
        productDetailArray = []
        
        for file in initialFile(directory):
                # print('start: '+file)
                with open(directory + file)as f:
                        inn = f.read()
                productDetail = {}
                textSoup = BeautifulSoup(inn,'html.parser')
                productDetail['product_model'] = selectColumn(textSoup, 2).replace("\n","").replace(" ","")  #v
                productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": selectColumn(textSoup, 3).replace("公升", " L"), 
                                                                        "warm_water_system_storage_tank_capacity_indication_value": selectColumn(textSoup, 4).replace("公升", " L").replace('\t',''),
                                                                        "est,24": selectColumn(textSoup, 5).replace("(kWh/24小時)", " kWh/24hr")}
                productDetail["efficiency_benchmark"] = selectColumn(textSoup, 7) #v
                productDetail["annual_power_consumption_degrees_dive_year"] = searchFloatNums(selectColumn(textSoup, 10))#V
                productDetailArray.append(productDetail)
                # print('done: '+file)
        
        bureauEnergyDetail['productDetail'] = productDetailArray
        bureauEnergyDetail['keyword'] = searchword
        bureauEnergyDetail["dateTime"] = timeStampGenerator()

        totalNums = len(bureauEnergyDetail['productDetail'])

        return bureauEnergyDetail, totalNums


