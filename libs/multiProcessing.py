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


def distributeKeyword(keywordUrlPair, output):
    for keyword in keywordUrlPair:
        print('distributeKeyword in main process %s' %os.getpid())
        output.put(keyword)
        print("這裡是distributeKeyword，準備送給  接下來的進程  處理: " + keyword)
        timeSleepOne() #暫停幾秒來模擬現實狀況。



_monthsAvailable = [str(row) for row in range(1,13)]

_weatherRecordAvailable = {"2009": _monthsAvailable,
                        "2010": _monthsAvailable,
                        "2011": _monthsAvailable,
                        "2012": _monthsAvailable,
                        "2013": _monthsAvailable,
                        "2014": _monthsAvailable,
                        "2015": _monthsAvailable,
                        "2016": _monthsAvailable,
                        "2017": _monthsAvailable,
                        "2018": _monthsAvailable,
                        "2019": [str(row) for row in range(1,6)]}

_bureauEnergyKeywordUrlPair = {"無風管空氣調節機":("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
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

_googleSearchWord = {"家電促銷":"",
                     "家電汰舊換新":"",
                     "家電節能補助":""}


_momoKeywordUrlPair = {"溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
                        "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType")}


# _momoKeywordUrlPair = {"冷暖空調":("https://www.momoshop.com.tw/search/searchShop.jsp"
#                         "?keyword=%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF"
#                         "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
#                 "除濕機":("https://www.momoshop.com.tw/search/searchShop.jsp"
#                         "?keyword=%E9%99%A4%E6%BF%95%E6%A9%9F"
#                         "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
#                 "電冰箱":("https://www.momoshop.com.tw/search/searchShop.jsp"
#                         "?keyword=%E9%9B%BB%E5%86%B0%E7%AE%B1"
#                         "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
#                 "電熱水瓶":("https://www.momoshop.com.tw/search/searchShop.jsp"
#                         "?keyword=%E9%9B%BB%E7%86%B1%E6%B0%B4%E7%93%B6"
#                         "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
#                 "溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
#                         "?keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
#                         "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
#                 "溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp?"
#                         "keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
#                         "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
#                 "冰溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
#                                 "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
#                                 "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
#                 "冰溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp"
#                                 "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
#                                 "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType")}

_pchomeKeywordUrlPair = {"冷暖空調":"",
                         "除濕機":"",
                         "電冰箱":"",
                         "電熱水瓶":"",
                         "溫熱型開飲機":"",
                         "溫熱型飲水機":"",
                         "冰溫熱型開飲機":"",
                         "冰溫熱型飲水機":""}


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




