# -*- coding:utf-8 -*-

"""
程式名稱： insertHistoricalDataIntoDB.py
程式描述：


備　　註：

    
    歷史檔案 能源局 52個 花費： 916.3982834815979 秒。

    將 classBureauEnergyProductsWholeTable 直接一列一列倒進去  bureauEnergyProductsBackup表格裡，花費：293.0093584060669 秒。


    歷史檔案 pchome 36個 花費： 7635.215828180313 秒。

    歷史檔案 momo   44個 花費： 3170.492326974869 秒

    最新檔案 pchome, momo 花費： 320.7821488380432 秒。



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

def writeBureauHistoricalData(multiSourceObject, sourceDataFolderName=None, bureauSET=None, alterStillWork=None):

    """
    PART (1)-1
    歷史檔案 能源局產品 寫入bureau_energy_products_backup 表格-------------------------------------

    This session is one-time procedure!   No need to do it again if done.
    """

    if not alterStillWork:
        begin = timeCalculate()
        multiSourceObject.writeHistoricalDataIntoDB(multiSourceObject.bureauEnergyM, 
                            sourceDataFolderName=sourceDataFolderName, bureauSET=bureauSET)
        end = timeCalculate()
        print(f"歷史檔案 {sourceDataFolderName} 花費：", end-begin, "秒。")

    else:

        """
        PART (1)-2
        最新檔案 能源局產品  寫入bureau_energy_products_backup 表格-------------------------------------

        This session is alternative;We are allowed to execute programs here or at "insertLatestDataIntoDB.py  PART (2)-2"。
        What worth giving attention is whether historical data in DB at first?
        """


        begin = timeCalculate()
        multiSourceObject.bureauEnergyM.alterStillWorkToZero(alterStillWork)
        multiSourceObject.writeHistoricalDataIntoDB(multiSourceObject.bureauEnergyM, 
                            sourceDataFolderName=sourceDataFolderName, bureauSET=bureauSET, latestBoolean=1)
        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName} 花費：", end-begin, "秒。")



def writeEcommerceHistoricalData(multiSourceObject, sourceDataFolderName_1=None, sourceDataFolderName_2=None, alterStillWork=None):
    
    
    """
    PART (2)-1
    歷史檔案 電商產品 寫入 ecommerce_products_backup 表格 
    ----------連同價格異動的情況送進 ecommerce_products_price_records資料表--------------------------
    This session is one-time procedure!   No need to do it again if done.
    """
    if not alterStillWork:
        begin = timeCalculate()
        multiSourceObject.writeHistoricalDataIntoDB(multiSourceObject.ecommerceM, 
                                        sourceDataFolderName=sourceDataFolderName_1)
        end = timeCalculate()
        print(f"歷史檔案 {sourceDataFolderName_1} 花費：", end-begin, "秒。")


        begin = timeCalculate()
        multiSourceObject.writeHistoricalDataIntoDB(multiSourceObject.ecommerceM, 
                                        sourceDataFolderName=sourceDataFolderName_2)
        end = timeCalculate()
        print(f"歷史檔案 {sourceDataFolderName_2} 花費：", end-begin, "秒。")

    else:
        """
        PART (2)-2
        最新檔案 電商產品 寫入 ecommerce_products_backup 表格 
        -----------連同價格異動的情況送進 ecommerce_products_price_records資料表--------------------------
        This session is alternative;We are allowed to execute programs here or at "insertLatestDataIntoDB.py  PART (3)-2"。
        What worth giving attention is whether historical data in DB at first?
        """
        begin = timeCalculate()

        multiSourceObject.ecommerceM.alterStillWorkToZero(alterStillWork)
        multiSourceObject.writeHistoricalDataIntoDB(multiSourceObject.ecommerceM, 
                                        sourceDataFolderName=sourceDataFolderName_1, latestBoolean=1)
        end = timeCalculate()
        print(f"最新檔案 {sourceDataFolderName_1}, {sourceDataFolderName_2} 花費：", end-begin, "秒。")








if __name__ == '__main__':
    tableClassBase = writeDataWhenMunging._tableClassBase

    engine = sqlObjectInitial.loadCorrectEngine(tableClassBase, tableClassBase.databaseName)
    
    multiSourceObject = multiSourceObjectInitial(bureauEnergyM=bureauEnergyMungingHistorical(), 
                                        ecommerceM=ecommerceMungingHistorical())
    
    bureauEnergyFolder = multiSourceObject.bureauEnergyM._objectiveBureauEnergy
    pchomeFoler = multiSourceObject.ecommerceM._objectivePchome
    momoFolder = multiSourceObject.ecommerceM._objectiveMomo
    
    
    #-------------------------------------

    """
    PART (1)-1 This session is one-time procedure!   No need to do it again if done.
    """
    writeBureauHistoricalData(multiSourceObject, 
                        sourceDataFolderName=bureauEnergyFolder, bureauSET=bureauSET())
  

    """
    PART (1)-2 This session is alternative;
    We are allowed to execute programs here or at "insertLatestDataIntoDB.py  PART (2)-2"。
    What worth giving attention is whether historical data in DB at first?
    """
    writeBureauHistoricalData(multiSourceObject, 
                        sourceDataFolderName=bureauEnergyFolder, bureauSET=bureauSET(), alterStillWork=1)


    """
    PART (2)-1 This session is one-time procedure!   No need to do it again if done.
    """
    
    writeEcommerceHistoricalData(multiSourceObject, 
                        sourceDataFolderName_1=pchomeFoler, sourceDataFolderName_2=momoFolder)

    """
    PART (2)-2 This session is alternative;
    We are allowed to execute programs here or at "insertLatestDataIntoDB.py  PART (3)-2"。
    What worth giving attention is whether historical data in DB at first?
    """
    writeEcommerceHistoricalData(multiSourceObject, 
                        sourceDataFolderName_1=pchomeFoler, sourceDataFolderName_2=momoFolder, alterStillWork=1)


