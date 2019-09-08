# -*- coding:utf-8 -*-

"""
程式名稱： insertLatestDataIntoDB.py
程式描述：


備　　註：

    新檔案 bureauEnergy 花費： 242.81847214698792 秒。

    能源局 、pchome、momo 花費： 3356.2910916805267 秒

"""

import os
import sys
import json
from sqlalchemy.orm import sessionmaker


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.sqlDDLAndsqlAlchemyORM import (
                                        sqlORMForTables,
                                        sqlObjectInitial
                                        )
from libs.sqlDMLAndsqlAlchemyORM import (
                                        referenceFiles, 
                                        bureauEnergyMunging, 
                                        bureauEnergyMungingHistorical,
                                        ecommerceMunging,
                                        ecommerceMungingHistorical,
                                        weatherMunging,
                                        newsTitleFromSeleniumMunging,
                                        selectedNewsContentMunging,
                                        multiSourceObjectInitial,
                                        writeDataWhenMunging
                                        )
from libs.timeWidget import timeCalculate
from libs.munging import bureauEnergyMunging as bureauSET
from libs.manipulateDir import (
                                    initialFileZeroUnderscoreInt,
                                    initialFileFirstUnderscoreString,
                                    initialFileFourthUnderscoreString
                                )



def writeReferenceData(tableClassBase, engine):
    """
    PART (1)
    寫入 referenceFiles-------------------------------------
    This session is one-time procedure! No need to do it again if done.
    """
    begin = timeCalculate()
    referenceFiles().writeReferenceDataIntoDB(tableClassBase, engine)
    end = timeCalculate()

    print("referenceFiles完成：", end-begin, "秒。")



def writeBureauData(multiSourceObject, sourceDataFolderName=None, bureauSET=None, alterStillWork=None):

    """
    PART (2)-1
    寫入 能源局產品 到 bureau_energy_products 表格-------------------------------------
    This session is one-time procedure and have to be done repeatedly if having the latest files.
    """
    if not alterStillWork: # 塞 最新的表
        begin = timeCalculate()
        multiSourceObject.bureauEnergyM.truncateTable(1, sourceDataFolderName=sourceDataFolderName)
        multiSourceObject.writeLatestDataIntoDB(multiSourceObject.bureauEnergyM, 
                        sourceDataFolderName=sourceDataFolderName, bureauSET=bureauSET)
        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName} 花費：", end-begin, "秒。")
    else: # 塞 backup表
        """
        PART (2)-2
        將最新的 能源局產品 檔案寫入bureau_energy_products_backup 表格
        This session is alternative;Please refer to 'inserHistoricalDataIntoDB.py  PART (1)-2".
        """
        begin = timeCalculate()
        multiSourceObject.bureauEnergyM.alterStillWorkToZero(alterStillWork)
        multiSourceObject.writeHistoricalDataIntoDB(multiSourceObject.bureauEnergyM, 
                            sourceDataFolderName=sourceDataFolderName, bureauSET=bureauSET, latestBoolean=1)
        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName} 寫入backup表格 花費：", end-begin, "秒。")



def writeEcommerceData(multiSourceObject, sourceDataFolderName_1=None, sourceDataFolderName_2=None, alterStillWork=None):

    """
    PART (3)-1
    寫入 電商商品 到 ecommerce_products 表格-------------------------------------
    This session is one-time procedure and have to be done repeatedly if having the latest files.
    """
    if not alterStillWork:  # 塞 最新的表
        begin = timeCalculate()
        multiSourceObject.ecommerceM.truncateTable(1, sourceDataFolderName=sourceDataFolderName_1)
        multiSourceObject.writeLatestDataIntoDB(multiSourceObject.ecommerceM,
                        sourceDataFolderName=sourceDataFolderName_1)
        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName_1} 花費：", end-begin, "秒。")

        begin = timeCalculate()
        multiSourceObject.writeLatestDataIntoDB(multiSourceObject.ecommerceM, 
                        sourceDataFolderName=sourceDataFolderName_2)
        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName_2} 花費：", end-begin, "秒。")
    
    else:  # 塞 backup表

        """
        PART (3)-2
        將最新的 電商商品 檔案寫入 ecommerce_products_backup 表格 ----------連同價格異動的情況送進 ecommerce_products_price_records資料表--------------------------
        This session is alternative;Please refer to 'inserHistoricalDataIntoDB.py PART (2)-2".
        """

        begin = timeCalculate()

        multiSourceObject.ecommerceM.alterStillWorkToZero(alterStillWork)
        multiSourceObject.writeHistoricalDataIntoDB(multiSourceObject.ecommerceM, 
                                        sourceDataFolderName=sourceDataFolderName_1, latestBoolean=1)
        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName_1}, {sourceDataFolderName_2} 花費：", end-begin, "秒。")




def writeWeatherData(multiSourceObject, sourceDataFolderName=None):
    """
    PART (4)
    將氣象歷史資料 寫入  weather_records_by_months 表格-------------------------------------
    This session is one-time procedure  and have to be done repeatedly if having the latest files.
    """
    begin = timeCalculate()

    multiSourceObject.weatherM.truncateTable(1)
    multiSourceObject.writeLatestDataIntoDB(multiSourceObject.weatherM, 
                                    sourceDataFolderName=sourceDataFolderName)
    end = timeCalculate()
    print(f"最新檔案 {sourceDataFolderName} 花費：", end-begin, "秒。")



def writeNewsTitle(multiSourceObject, sourceDataFolderName=None, historyFile=None):
    """
    PART (5)-1
    將 新聞標題 歷史資料 寫入 news_title_from_selenium 表格-------------------------------------
    This session is one-time procedure!  No need to do it again if done.
    """
    if historyFile:
        begin = timeCalculate()

        multiSourceObject.newsM.truncateTable(1, sourceDataFolderName=sourceDataFolderName)
        multiSourceObject.writeLatestDataIntoDB(multiSourceObject.newsM, 
                                        sourceDataFolderName=sourceDataFolderName)
        end = timeCalculate()
        print(f"歷史檔案 {sourceDataFolderName} 花費：", end-begin, "秒。")

    else:
        """
        PART (5)-2
        將 新聞標題 最新的資料 寫入 news_title_from_selenium 表格-------------------------------------
        This session is one-time procedure and have to be done repeatedly if having the latest files.
        """
        begin = timeCalculate()

        multiSourceObject.writeLatestDataIntoDB(multiSourceObject.newsM, 
                                        sourceDataFolderName=sourceDataFolderName, latestBoolean=1)
        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName} 花費：", end-begin, "秒。")



def writeNewsContent(multiSourceObject, sourceDataFolderName=None, historyFile=None):
    """
    PART (6)-1
    將 篩選的新聞 歷史資料 寫入 selected_news_with_tfidf 表格-------------------------------------
    This session is one-time procedure!  No need to do it again if done.
    """
    if historyFile:

        begin = timeCalculate()

        multiSourceObject.newsWithContentM.truncateTable(1, sourceDataFolderName=sourceDataFolderName)
        multiSourceObject.writeLatestDataIntoDB(multiSourceObject.newsWithContentM, 
                                        sourceDataFolderName=sourceDataFolderName)

        end = timeCalculate()
        print(f"歷史檔案 {sourceDataFolderName} 花費：", end-begin, "秒。")

    else:
        """
        PART (6)-2
        將 篩選的新聞 最新的資料 寫入 selected_news_with_tfidf 表格-------------------------------------
        This session is one-time procedure and have to be done repeatedly if having the latest files.
        """

        begin = timeCalculate()

        multiSourceObject.writeLatestDataIntoDB(multiSourceObject.newsWithContentM,
                                    sourceDataFolderName=sourceDataFolderName, latestBoolean=1)

        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName} 花費：", end-begin, "秒。")



if __name__ == '__main__':
    tableClassBase = writeDataWhenMunging._tableClassBase
    engine = sqlObjectInitial.loadCorrectEngine(tableClassBase, tableClassBase.databaseName)
    
    multiSourceObject = multiSourceObjectInitial(bureauEnergyM=bureauEnergyMunging(), 
                                                ecommerceM=ecommerceMunging(), 
                                                weatherM=weatherMunging(), 
                                                newsM=newsTitleFromSeleniumMunging(),
                                                newsWithContentM=selectedNewsContentMunging())

    multiSourceObjectForBackupTable = multiSourceObjectInitial(bureauEnergyM=bureauEnergyMungingHistorical(), 
                                                            ecommerceM=ecommerceMungingHistorical())
    
    bureauEnergyFolder = multiSourceObject.bureauEnergyM._objectiveBureauEnergy
    pchomeFoler = multiSourceObject.ecommerceM._objectivePchome
    momoFolder = multiSourceObject.ecommerceM._objectiveMomo
    weatherFolder = multiSourceObject.weatherM._objectiveWeather
    newsIntegraFolder = multiSourceObject.newsM._objectiveNewsIntegra
    newsWithContentFolder = multiSourceObject.newsWithContentM._objectiveNewsWithContent
    

    
    # """
    # PART (1) This session is one-time procedure! No need to do it again if done.
    # """
    # writeReferenceData(tableClassBase, engine)

    # """
    # PART (2)-1 This session is one-time procedure and have to be done repeatedly if having the latest files.
    # """
    # writeBureauData(multiSourceObject, 
    #                         sourceDataFolderName=bureauEnergyFolder, bureauSET=bureauSET())
    
    # """
    # PART (2)-2 This session is alternative;Please refer to 'inserHistoricalDataIntoDB.py  PART (1)-2".
    # """
    # writeBureauData(multiSourceObjectForBackupTable, 
    #                         sourceDataFolderName=bureauEnergyFolder, bureauSET=bureauSET(), alterStillWork=1)


    # """
    # PART (3)-1 This session is one-time procedure and have to be done repeatedly if having the latest files.
    # """
    # writeEcommerceData(multiSourceObject, 
    #                         sourceDataFolderName_1=pchomeFoler, sourceDataFolderName_2=momoFolder)



    # """
    # PART (3)-2 This session is alternative;Please refer to 'inserHistoricalDataIntoDB.py PART (2)-2".
    # """
    # writeEcommerceData(multiSourceObjectForBackupTable, 
    #                         sourceDataFolderName_1=pchomeFoler, sourceDataFolderName_2=momoFolder, alterStillWork=1)


    # """
    # PART (4) This session is one-time procedure  and have to be done repeatedly if having the latest files.
    # """
    # writeWeatherData(multiSourceObject,
    #                         sourceDataFolderName=weatherFolder)

    # """
    # PART (5)-1 This session is one-time procedure!  No need to do it again if done.
    # """
    # writeNewsTitle(multiSourceObject, 
    #                         sourceDataFolderName=newsIntegraFolder, historyFile=1)
    # """

    # PART (5)-2 This session is one-time procedure and have to be done repeatedly if having the latest files.
    # """
    # writeNewsTitle(multiSourceObject, 
    #                         sourceDataFolderName=newsIntegraFolder)



    # """
    # PART (6)-1 This session is one-time procedure!  No need to do it again if done.
    # """
    # writeNewsContent(multiSourceObject, 
    #                         sourceDataFolderName=newsWithContentFolder, historyFile=1)
    # """
    # PART (6)-2 This session is one-time procedure and have to be done repeatedly if having the latest files.
    # """
    # writeNewsContent(multiSourceObject, 
    #                         sourceDataFolderName=newsWithContentFolder)
    










    # conn = engine.connect()

    # # result = conn.execute(f"select product_model from {tableClassBase.table2} where 3C_Id = {1}".format("1"))
    # Session = sessionmaker(bind=conn)
    # session = Session()

    # # rows = result.fetchall()
    # # print(rows[-5:])

    # # result = ecommerceMunging().getReferenceTupleFromDB(tableClassBase,session, "1")
    # # print(result[-100:])
    # obj = session.query(tableClassBase.bureauEnergyProducts).filter(tableClassBase.bureauEnergyProducts.product_model=="18356＋UN-1322AG-1").first()
    # print(obj.product_model)

    # session.close()
    # conn.close()