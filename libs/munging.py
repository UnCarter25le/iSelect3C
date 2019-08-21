# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.timeWidget import timeSleepOne
from libs.timeWidget import timeStampGenerator
from libs.manipulateDir import initialFile
# from libs.regex import interDiv
# from libs.regex import searchFloatNums
# from libs.regex import searchNums
# from libs.regex import floatDiv
from libs.regex import bureauEnergyReplace
from libs.regex import numsHandler



bureauReplace = bureauEnergyReplace()
numsHandler = numsHandler()


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



class bureauEnergyMunging(object):
        @classmethod
        def selectColumn(cls, textSoup, row):
                selected = textSoup.find('div',{'class':'row text-center col-sm-12'}).select('.row')[row].text
                selected = selected.split('：')[1]
                return selected

        @classmethod
        def energyLabelUrl(cls):
                return "https://ranking.energylabel.org.tw/_Upload/applyMain/applyp/"



        def detailMungingEntry(self, searchword, directory):
                bureauEnergyDetail = {}
                productDetailArray = []
                labelUrl = bureauEnergyMunging.energyLabelUrl()

                if searchword == "除濕機":
                        productDetailArray = self.detailDehumidification_2(productDetailArray, directory,labelUrl)
                elif searchword == "無風管空氣調節機":
                        productDetailArray = self.detailAirConditioner_2(productDetailArray, directory,labelUrl)
                elif searchword == "電冰箱":
                        productDetailArray = self.detailRefrigerator_2(productDetailArray, directory,labelUrl)
                elif searchword == "電熱水瓶":
                        productDetailArray = self.detailElectricWarmer_2(productDetailArray, directory,labelUrl)
                elif searchword == "溫熱型開飲機":
                        productDetailArray = self.detailWarmDrinkMachine_2(productDetailArray, directory,labelUrl)
                elif searchword == "溫熱型飲水機":
                        productDetailArray = self.detailWarmDispenser_2(productDetailArray, directory,labelUrl)
                elif searchword == "冰溫熱型開飲機":
                        productDetailArray = self.detailColdWarmDrinkMachine_2(productDetailArray, directory,labelUrl)
                elif searchword == "冰溫熱型飲水機":
                        productDetailArray = self.detailColdWarmDispenser_2(productDetailArray, directory,labelUrl)
                elif searchword == "貯備型電熱水器":
                        productDetailArray = self.detailStorageWaterHeaters_2(productDetailArray, directory,labelUrl)
                elif searchword == "瓦斯熱水器":
                        productDetailArray = self.detailGasWaterHeaters_2(productDetailArray, directory,labelUrl)
                elif searchword == "瓦斯爐":
                        productDetailArray = self.detailGasStove_2(productDetailArray, directory,labelUrl)
                elif searchword == "安定器內藏式螢光燈泡":
                        productDetailArray = self.detailCompactFluorescentLamp_2(productDetailArray, directory,labelUrl)
                
                bureauEnergyDetail['productDetail'] = productDetailArray
                bureauEnergyDetail['keyword'] = searchword
                bureauEnergyDetail["dateTime"] = timeStampGenerator()

                totalNums = len(bureauEnergyDetail['productDetail'])

                return bureauEnergyDetail, totalNums
        
        #  detail 檔案裡面有髒值  冰箱"product_model": "B23KV-81RE\n",   "IB 7030 F TW" 空調"product_model": "PAX-K500CLD ",
        def detailDehumidification_2(self, productDetailArray, directory, labelUrl, *args): #除濕機
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                MD1631W	東元(TECO)	HDN-108-0022	東元電機股份有限公司	1	2019/07/18	有效
                
                『detailHTML』
                X1.標示義務公司：東元電機股份有限公司
                X2.產品類別：除濕機(107年新分級基準)
                O3.產品型號：MD1631W
                O4.額定除濕能力：8.0公升/日
                O5.能源因數值：2.4公升/千瓦小時公升
                X6.產品效率分級：第1級
                O7.最低能源效率基準：1.20 公升/千瓦小時
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：HDN-108-0022
                O10.年耗電量：75(度/年)

                `summary: {p1}/HDN_photo1/product_model_original.jpg`
                
                """
                for file in initialFile(directory):
                        #print("start: " + file)
                        with open(directory + file)as f:
                                inn = f.read()
                        
                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        #p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/HDN_photo1/{productModelOriginal}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)#v
                        productDetail["test_report_of_energy_efficiency"]  = {"rated_dehumidification_capacity": bureauReplace.capacityDay(bureauEnergyMunging.selectColumn(textSoup, 3)), 
                                                                        "energy_factor_value": bureauReplace.capacityHour(bureauEnergyMunging.selectColumn(textSoup, 4))}
                        productDetail["efficiency_benchmark"] = bureauReplace.capacityHourSpecial(bureauEnergyMunging.selectColumn(textSoup, 6))#v
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)

                        #print('done: ' + file)
                return productDetailArray
        
        # def detailDehumidification(self, searchword, directory): #除濕機
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 #print("start: " + file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()
                        
        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 #p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/HDN_photo1/{productModelOriginal}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)#v
        #                 productDetail["test_report_of_energy_efficiency"]  = {"rated_dehumidification_capacity": bureauReplace.capacityDay(bureauEnergyMunging.selectColumn(textSoup, 3)), 
        #                                                                 "energy_factor_value": bureauReplace.capacityHour(bureauEnergyMunging.selectColumn(textSoup, 4))}
        #                 productDetail["efficiency_benchmark"] = bureauReplace.capacityHourSpecial(bureauEnergyMunging.selectColumn(textSoup, 6))#v
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)

        #                 #print('done: ' + file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums


        def detailAirConditioner_2(self, productDetailArray, directory, labelUrl, *args): #無風管空氣調節機

                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                DAO-AG41	大井(Da Jing)	ACN-108-1079	台灣高沅空調科技股份有限公司	5	2019/07/18	有效
                
                『detailHTML』
                X1.標示義務公司：台灣高沅空調科技股份有限公司
                X2.產品類別：無風管空氣調節機
                O3.產品型號：DAO-AG41
                X4.冷氣機機組構成方式：一對一分離式
                O5.額定冷氣能力：4.1 kW
                X6.額定中間冷氣能力： kW
                O7.額定冷氣能力消耗電功率：1.192 kW
                X8.額定中間冷氣能力消耗電功率： kW
                O9.冷氣季節性能因數CSPF：3.60 kWh/kWh
                X10.室外機冷氣季節性能因數CSPF：
                O11.最低能源效率基準：3.60 kWh/kWh
                X12.是否符合最低能源效率基準：符合
                X13.登錄編號：ACN-108-1079
                O14.年耗電量：1353(度/年)

                `summary: {p1}/ACN_photo1/product_model_original.jpg`
                
                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()

                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        #p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/ACN_photo1/{productModelOriginal}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)
                        productDetail["test_report_of_energy_efficiency"] = {"rated_cooling_capacity": bureauEnergyMunging.selectColumn(textSoup, 4),
                                                                        "EER": str(numsHandler.floatDiv(bureauEnergyMunging.selectColumn(textSoup, 4), bureauEnergyMunging.selectColumn(textSoup, 6)))+' kW/kW', 
                                                                        "CSPF": bureauEnergyMunging.selectColumn(textSoup, 8)}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 10)
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 13))
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)

                        print('done: '+file) #無風管通常洗最久，保留才不會認為是程式當機了
                return productDetailArray

        # def detailAirConditioner(self, searchword, directory): #無風管空氣調節機
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()

        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()

        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 #p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/ACN_photo1/{productModelOriginal}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)
        #                 productDetail["test_report_of_energy_efficiency"] = {"rated_cooling_capacity": bureauEnergyMunging.selectColumn(textSoup, 4),
        #                                                                 "EER": str(numsHandler.floatDiv(bureauEnergyMunging.selectColumn(textSoup, 4), bureauEnergyMunging.selectColumn(textSoup, 6)))+' kW/kW', 
        #                                                                 "CSPF": bureauEnergyMunging.selectColumn(textSoup, 8)}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 10)
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 13))
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)

        #                 print('done: '+file) #無風管通常洗最久，保留才不會認為是程式當機了
        
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums


        def detailRefrigerator_2(self, productDetailArray, directory, labelUrl, *args): #電冰箱
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                SR-B58D	聲寶(SAMPO)	RFN-108-0071	聲寶股份有限公司	1	2019/07/18	有效
                
                『detailHTML』
                X1.標示義務公司：聲寶股份有限公司
                X2.產品類別：電冰箱(107年新分級基準)
                O3.產品型號：SR-B58D
                O4.有效內容積：580公升
                O5.能源因數值：26.2公升/度/月
                X6.產品效率分級：第1級
                O7.最低能源效率基準：16.4 公升/度/月
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：RFN-108-0071
                O10.年耗電量：312(度/年)
                        
 
                `summary: {p1}/RFn_photo1/product_model_original.jpg`
                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()

                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        #p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/RFn_photo1/{productModelOriginal}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)  #v
                        productDetail["test_report_of_energy_efficiency"]  = {"effective_internal_volume": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
                                                                                "energy_factor_value": bureauReplace.capacityMonth(bureauEnergyMunging.selectColumn(textSoup, 4))}
                        productDetail["efficiency_benchmark"] = bureauReplace.capacityMonthSpecial(bureauEnergyMunging.selectColumn(textSoup, 6)) 
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailRefrigerator(self, searchword, directory): # 電冰箱
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()

        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 #p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/RFn_photo1/{productModelOriginal}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)  #v
        #                 productDetail["test_report_of_energy_efficiency"]  = {"effective_internal_volume": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
        #                                                                         "energy_factor_value": bureauReplace.capacityMonth(bureauEnergyMunging.selectColumn(textSoup, 4))}
        #                 productDetail["efficiency_benchmark"] = bureauReplace.capacityMonthSpecial(bureauEnergyMunging.selectColumn(textSoup, 6)) 
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums


        def detailElectricWarmer_2(self, productDetailArray, directory, labelUrl, *args): #電熱水瓶
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                CV-DXF40	象印(ZOJIRUSHI)	TB-108-0003	台象股份有限公司	1	2019/05/08	有效
                
                『detailHTML』
                X1.標示義務公司：台象股份有限公司
                X2.產品類別：電熱水瓶
                O3.產品型號：CV-DXF40
                O4.有效內容積：4.0公升
                O5.每24小時標準化備用損失Est,24(標示登錄值)：0.572(kWh/24小時)
                X6.產品效率分級：第1級
                O7.最低能源效率基準：1.372
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：TB-108-0003
                O9.年耗電量：209(度/年)
                
                `summary: {p1}/TB_photo1/product_model_original.jpg`
   
                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()

                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        #p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/TB_photo1/{productModelOriginal}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)  #v
                        productDetail["test_report_of_energy_efficiency"]  = {"effective_internal_volume": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
                                                                                "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 4))}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6) + " kWh/24hr"#v
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailElectricWarmer(self, searchword, directory): #電熱水瓶
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()

        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 #p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/TB_photo1/{productModelOriginal}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)  #v
        #                 productDetail["test_report_of_energy_efficiency"]  = {"effective_internal_volume": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
        #                                                                         "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 4))}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6) + " kWh/24hr"#v
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums


        def detailWarmDrinkMachine_2(self, productDetailArray, directory, labelUrl, *args): #溫熱型開飲機
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                YS-8308DW	元山	WD-108-0012	元山科技工業股份有限公司	4	2019/05/17	有效
                
                『detailHTML』
                
                X1.標示義務公司：元山科技工業股份有限公司
                X2.產品類別：溫熱型開飲機
                O3.產品型號：YS-8308DW
                O4.熱水系統貯水桶容量標示值：5.4公升
                O5.每24小時標準化備用損失Est,24(標示登錄值)：1.8(kWh/24小時)
                X6.產品效率分級：第4級
                O7.最低能源效率基準：2.013
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：WD-108-0012
                O10.每年保溫耗電量：657(度/年)
                 
                `summary: {p1}/WD_photo1/product_model_original_{p0}.jpg`

                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()

                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/WD_photo1/{productModelOriginal}_{p0}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)#v
                        productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
                                                                                "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 4))}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6) + " kWh/24hr" #v
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailWarmDrinkMachine(self, searchword, directory): #溫熱型開飲機
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()

        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/WD_photo1/{productModelOriginal}_{p0}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)#v
        #                 productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
        #                                                                         "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 4))}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6) + " kWh/24hr" #v
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums

        def detailWarmDispenser_2(self, productDetailArray, directory, labelUrl, *args): #溫熱型飲水機
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                LP-CH-806(110V)	力霸	WF-108-0068	力霸工業科技股份有限公司	1	2019/07/10	有效
                
                『detailHTML』
                X1.標示義務公司：力霸工業科技股份有限公司
                X2.產品類別：溫熱型飲水機
                O3.產品型號：LP-CH-806(110V)
                O4.熱水系統貯水桶容量標示值：24公升
                O5.每24小時標準化備用損失Est,24(標示登錄值)：1(kWh/24小時)
                X6.產品效率分級：第1級
                O7.最低能源效率基準：2.022
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：WF-108-0068
                O10.每年保溫耗電量：365(度/年)
                

                `summary: {p1}/WF_photo1/product_model_original_{p0}.jpg`

                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()

                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/WF_photo1/{productModelOriginal}_{p0}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)  #v
                        productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
                                                                                "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 4))}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6) + " kWh/24hr"#v
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailWarmDispenser(self, searchword, directory):#溫熱型飲水機
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()

        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/WF_photo1/{productModelOriginal}_{p0}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)  #v
        #                 productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
        #                                                                         "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 4))}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6) + " kWh/24hr"#v
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))#V
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums

        def detailColdWarmDrinkMachine_2(self, productDetailArray, directory, labelUrl, *args): #冰溫熱型開飲機
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                AP-9061		WW-108-0001	豪品電器股份有限公司	5	2019/04/25	有效
                
                『detailHTML』
                X1.標示義務公司：豪品電器股份有限公司
                X2.產品類別：冰溫熱型開飲機
                O3.產品型號：AP-9061
                O4.熱水系統貯水桶容量標示值：4.6公升
                O5.溫水貯水桶容量標示值： 1.3公升
                O6.每24小時標準化備用損失Est,24(標示登錄值)：1.888(kWh/24小時)
                X7.產品效率分級：第5級
                O8.最低能源效率基準：1.942
                X9.是否符合最低能源效率基準：符合
                X10.登錄編號：WW-108-0001
                O11.每年保溫耗電量：689(度/年)

                `summary: {p1}/WW_photo1/product_model_original_{p0}.jpg`
                
                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()
                        
                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/WW_photo1/{productModelOriginal}_{p0}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)#v
                        productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
                                                                                "warm_water_system_storage_tank_capacity_indication_value": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 4)),
                                                                                "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 5))}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 7) + " kWh/24hr"#v
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 10))#V
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailColdWarmDrinkMachine(self, searchword, directory): #冰溫熱型開飲機
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()
                        
        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/WW_photo1/{productModelOriginal}_{p0}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)#v
        #                 productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
        #                                                                         "warm_water_system_storage_tank_capacity_indication_value": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 4)),
        #                                                                         "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 5))}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 7) + " kWh/24hr"#v
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 10))#V
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums

        def detailColdWarmDispenser_2(self, productDetailArray, directory, labelUrl, *args): #冰溫熱型飲水機
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                LP-CH-903(110V)	力霸	DF-108-0018	力霸工業科技股份有限公司	1	2019/07/12	有效

                『detailHTML』
                X1.標示義務公司：力霸工業科技股份有限公司
                X2.產品類別：冰溫熱型飲水機
                O3.產品型號：LP-CH-803CA(110V)附RO逆滲透純水機
                型號就是那麼長！
                https://ranking.energylabel.org.tw/_Upload/applyMain/applyp/20478/DF_photo1//LP-CH-803CA(110V)%E9%99%84RO%E9%80%86%E6%BB%B2%E9%80%8F%E7%B4%94%E6%B0%B4%E6%A9%9F_80999.jpg

                O4.熱水系統貯水桶容量標示值：20公升
                O5.冰水貯水桶容量標示值：4公升
                O6.每24小時標準化備用損失Est,24(標示登錄值)：1.1(kWh/24小時)
                X7.產品效率分級：第1級
                O8.最低能源效率基準：2.168
                X9.是否符合最低能源效率基準：符合
                X10.登錄編號：DF-108-0020
                O11.每年保溫耗電量：402(度/年)

                `summary: {p1}/DF_photo1/product_model_original_{p0}.jpg`

                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()

                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/DF_photo1/{productModelOriginal}_{p0}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)  #v
                        productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value":  bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
                                                                                "warm_water_system_storage_tank_capacity_indication_value":  bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 4)),
                                                                                "est,24":  bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 5))}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 7) + " kWh/24hr"#v
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 10))#V
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailColdWarmDispenser(self, searchword, directory): #冰溫熱型飲水機
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()

        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/DF_photo1/{productModelOriginal}_{p0}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)  #v
        #                 productDetail["test_report_of_energy_efficiency"]  = {"hot_water_system_storage_tank_capacity_indication_value":  bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)), 
        #                                                                         "warm_water_system_storage_tank_capacity_indication_value":  bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 4)),
        #                                                                         "est,24":  bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 5))}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 7) + " kWh/24hr"#v
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 10))#V
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums


        def detailStorageWaterHeaters_2(self, productDetailArray, directory, labelUrl, *args): #貯備型電熱水器
                """

                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                AH-1035W	兆豐	SWH-108-0340	遠鋒科技股份有限公司	5	2019/07/18	有效

                『detailHTML』
                X1.標示義務公司：阿里斯頓股份有限公司
                X2.產品類別：貯備型電熱水器
                O3.產品型號：QB R 80 V 2,5K TW
                產品型號就真是如此：QB R 80 V 2,5K TW
                https://ranking.energylabel.org.tw/_Upload/applyMain/applyp/20953/SWH_photo1/QB%20R%2080%20V%202,5K%20TW.jpg

                O4.內桶容量：80公升
                O5.每24小時標準化備用損失Est,24(標示登錄值)：0.8375(kWh/24小時)
                X6.產品效率分級：第3級
                O7.最低能源效率基準：1.09 Est,24 (度，kWh)    ；「Est,24 (度，kWh)」給去掉，replace("(kWh/24小時)", " kWh/24hr")
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：SWH-108-0338
                O10.年耗電量：306(度/年)

                `summary: {p1}/SWH_photo1/product_model_original.jpg`
                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()
                        
                        # 處理soup=""的情況
                        if not inn:
                                continue

                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        #p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/SWH_photo1/{productModelOriginal}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)
                        productDetail["test_report_of_energy_efficiency"]  = {"bucket_capacity": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)),
                                                                                "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 4))}
                        productDetail["efficiency_benchmark"] = bureauReplace.est24Special(bureauEnergyMunging.selectColumn(textSoup, 6))
                        productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailStorageWaterHeaters(self, searchword, directory): #貯備型電熱水器
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()
                        
        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue

        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 #p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/SWH_photo1/{productModelOriginal}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)
        #                 productDetail["test_report_of_energy_efficiency"]  = {"bucket_capacity": bureauReplace.capacity(bureauEnergyMunging.selectColumn(textSoup, 3)),
        #                                                                         "est,24": bureauReplace.est24(bureauEnergyMunging.selectColumn(textSoup, 4))}
        #                 productDetail["efficiency_benchmark"] = bureauReplace.est24Special(bureauEnergyMunging.selectColumn(textSoup, 6))
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = numsHandler.searchFloatNums(bureauEnergyMunging.selectColumn(textSoup, 9))
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums

        def detailGasWaterHeaters_2(self, productDetailArray, directory, labelUrl, *args): #瓦斯熱水器(即熱式燃氣熱水器)
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                HT-301B(LPG/RF式) `廠牌無名`		WH-108-0040	同順工業有限公司	3	2019/06/04	有效
                
                『detailHTML』
                X1.標示義務公司：同順工業有限公司
                X2.產品類別：瓦斯熱水器(即熱式燃氣熱水器)
                O3.產品型號：HT-301B(LPG/RF式)
                O4.燃氣別：液化石油氣(LPG)
                O5.標示熱效率：79.1 %
                X6.產品效率分級：第3級
                O7.最低能源效率基準：75.0 %
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：WH-108-0040

                `summary: {p1}/WH_photo1/product_model_original(斜線變底線)_{p0}.jpg`
                
                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()
                        
                        # 處理soup=""的情況
                        if not inn:
                                continue
                        
                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        productModelReplace = productModelOriginal.replace("/","_")
                        labelUri = labelUrl + f"{p1}/WH_photo1/{productModelReplace}_{p0}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)
                        productDetail["test_report_of_energy_efficiency"]  = {"category_of_gas": bureauEnergyMunging.selectColumn(textSoup, 3),
                                                                                "marked_thermal_efficiency": bureauEnergyMunging.selectColumn(textSoup, 4)}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6)
                        productDetail["annual_power_consumption_degrees_dive_year"] = "None"
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailGasWaterHeaters(self, searchword, directory): #瓦斯熱水器(即熱式燃氣熱水器)
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()

        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()
                        
        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue
                        
        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 productModelReplace = productModelOriginal.replace("/","_")
        #                 labelUri = labelUrl + f"{p1}/WH_photo1/{productModelReplace}_{p0}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)
        #                 productDetail["test_report_of_energy_efficiency"]  = {"category_of_gas": bureauEnergyMunging.selectColumn(textSoup, 3),
        #                                                                         "marked_thermal_efficiency": bureauEnergyMunging.selectColumn(textSoup, 4)}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6)
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = "None"
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums
                
        def detailGasStove_2(self, productDetailArray, directory, labelUrl, *args): #瓦斯爐(燃氣台爐)
                """
                `overview and detail的型號標示不一樣！overview的才是完整的。`

                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                VG231220CA(LPG)	GAGGENAU	GB-108-0215	博西家用電器股份有限公司	4	2019/07/09	有效
                
                『detailHTML』
                X1.標示義務公司：博西家用電器股份有限公司
                X2.產品類別：瓦斯爐(燃氣台爐)
                O3.產品型號：VG232220CA
                O4.燃氣別：天然氣(NG1)
                O5.標示熱效率：46 %
                X6.產品效率分級：第3級
                O7.最低能源效率基準：43.0 %
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：GB-108-0216
                
                `summary: {p1}/GB_photo1/product_model_original(類別)_{p0}.jpg`
                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()
                        
                        # 處理soup=""的情況
                        if not inn:
                                continue
                        
                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        categoryOfGas = bureauEnergyMunging.selectColumn(textSoup, 3)
                        categoryOfGasExtract = bureauReplace.categoryExtract(categoryOfGas)

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/GB_photo1/{productModelOriginal + categoryOfGasExtract}_{p0}.jpg"

                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal) + categoryOfGasExtract
                        productDetail["test_report_of_energy_efficiency"]  = {"category_of_gas": categoryOfGas,
                                                                                "marked_thermal_efficiency": bureauEnergyMunging.selectColumn(textSoup, 4)}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6)
                        productDetail["annual_power_consumption_degrees_dive_year"] = "None"
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray

        # def detailGasStove(self, searchword, directory): #瓦斯爐(燃氣台爐)
                
        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()
                
        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()
                        
        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue
                        
        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 categoryOfGas = bureauEnergyMunging.selectColumn(textSoup, 3)
        #                 categoryOfGasExtract = bureauReplace.categoryExtract(categoryOfGas)

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/GB_photo1/{productModelOriginal + categoryOfGasExtract}_{p0}.jpg"

        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal) + categoryOfGasExtract
        #                 productDetail["test_report_of_energy_efficiency"]  = {"category_of_gas": categoryOfGas,
        #                                                                         "marked_thermal_efficiency": bureauEnergyMunging.selectColumn(textSoup, 4)}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6)
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = "None"
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums

        def detailCompactFluorescentLamp_2(self, productDetailArray, directory, labelUrl, *args): #安定器內藏式螢光燈泡
                """
                『overviewHTML』
                型號	廠牌名稱	登錄編號	標示義務公司	效率等級	登錄通過日期	核准原因
                EF2R-13DEX1		SB-108-0059	奕慶實業有限公司	3	2019/06/20	有效
                
                『detailHTML』
                
                X1.標示義務公司：奕慶實業有限公司
                X2.產品類別：安定器內藏式螢光燈泡
                O3.產品型號：EFS-23LEX1
                O4.額定功率：23.0 W
                O5.標示發光效率：68.0 lm/W
                X6.產品效率分級：第3級
                O7.最低能源效率基準：60.0 lm/W
                X8.是否符合最低能源效率基準：符合
                X9.登錄編號：SB-108-0068

                `summary: {p1}/SB_photo1/product_model_original.jpg`
                """
                for file in initialFile(directory):
                        # print('start: '+file)
                        with open(directory + file)as f:
                                inn = f.read()
                        
                        # 處理soup=""的情況
                        if not inn:
                                continue
                        
                        productDetail = {}
                        textSoup = BeautifulSoup(inn,'html.parser')

                        detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
                        parseLink = urlparse(detailTxtLink)
                        #p0 = parse_qs(parseLink.query)['p0'].pop() 
                        p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
                        productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
                        labelUri = labelUrl + f"{p1}/SB_photo1/{productModelOriginal}.jpg"
                        
                        productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)
                        productDetail["test_report_of_energy_efficiency"]  = {"rated_power": bureauEnergyMunging.selectColumn(textSoup, 3),
                                                                                "marked_luminous_efficiency": bureauEnergyMunging.selectColumn(textSoup, 4)}
                        productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6)
                        productDetail["annual_power_consumption_degrees_dive_year"] = "None"
                        productDetail["energy_efficiency_label_innerUri"] = labelUri
                        productDetailArray.append(productDetail)
                        # print('done: '+file)
                return productDetailArray
                
        # def detailCompactFluorescentLamp(self, searchword, directory): #安定器內藏式螢光燈泡
                

        #         bureauEnergyDetail = {}
        #         productDetailArray = []
        #         labelUrl = bureauEnergyMunging.energyLabelUrl()

        #         for file in initialFile(directory):
        #                 # print('start: '+file)
        #                 with open(directory + file)as f:
        #                         inn = f.read()
                        
        #                 # 處理soup=""的情況
        #                 if not inn:
        #                         continue
                        
        #                 productDetail = {}
        #                 textSoup = BeautifulSoup(inn,'html.parser')

        #                 detailTxtLink = textSoup.find('form',{"method":"post"}).attrs.get("action")
        #                 parseLink = urlparse(detailTxtLink)
        #                 #p0 = parse_qs(parseLink.query)['p0'].pop() 
        #                 p1 = parse_qs(parseLink.query)['id'].pop() #id是p1
        #                 productModelOriginal = bureauEnergyMunging.selectColumn(textSoup, 2)
        #                 labelUri = labelUrl + f"{p1}/SB_photo1/{productModelOriginal}.jpg"
                        
        #                 productDetail['product_model'] = bureauReplace.productModel(productModelOriginal)
        #                 productDetail["test_report_of_energy_efficiency"]  = {"rated_power": bureauEnergyMunging.selectColumn(textSoup, 3),
        #                                                                         "marked_luminous_efficiency": bureauEnergyMunging.selectColumn(textSoup, 4)}
        #                 productDetail["efficiency_benchmark"] = bureauEnergyMunging.selectColumn(textSoup, 6)
        #                 productDetail["annual_power_consumption_degrees_dive_year"] = "None"
        #                 productDetail["energy_efficiency_label_innerUri"] = labelUri
        #                 productDetailArray.append(productDetail)
        #                 # print('done: '+file)
                
        #         bureauEnergyDetail['productDetail'] = productDetailArray
        #         bureauEnergyDetail['keyword'] = searchword
        #         bureauEnergyDetail["dateTime"] = timeStampGenerator()

        #         totalNums = len(bureauEnergyDetail['productDetail'])

        #         return bureauEnergyDetail, totalNums


