# -*- coding:utf-8 -*-

"""
程式名稱： insertLatestDataIntoDB.py
程式描述：


備　　註：

    omo 花費： 3356.2910916805267 秒

"""

import os
import sys
import json
from sqlalchemy.orm import sessionmaker


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.sqlDDLAndsqlAlchemyORM import (
                                        sqlORMForTables,
                                        sqlObjectInitail
                                        )
from libs.sqlDMLAndsqlAlchemyORM import (
                                        referenceFiles, 
                                        bureauEnergyMunging, 
                                        ecommerceMunging,
                                        multiSourceObjectInitial
                                        )
from libs.timeWidget import timeCalculate
from libs.munging import bureauEnergyMunging as bureauSET
from libs.manipulateDir import (
                                    initialFileZeroUnderscoreInt,
                                    initialFileFirstUnderscoreString,
                                    initialFileFourthUnderscoreString
                                )


if __name__ == '__main__':
    tableClassBase = sqlObjectInitail()._tableClassBase
    engine = tableClassBase.connectToMySQLEngine()
    
    multiSourceObject = multiSourceObjectInitial(bureauEnergyM=bureauEnergyMunging(), ecommerceM=ecommerceMunging())
    
    bureauEnergyFolder = multiSourceObject.bureauEnergyM._objectiveBureauEnergy
    pchomeFoler = multiSourceObject.ecommerceM._objectivePchome
    momoFolder = multiSourceObject.ecommerceM._objectiveMomo
    
    
    begin = timeCalculate()

    #-------------------------------------

    # # 插入 referenceFiles-------------------------------------
    # referenceFiles().writeReferenceDataIntoDB(tableClassBase, engine)
    # end = timeCalculate()

    # print("referenceFiles完成：", end-begin, "秒。")



    # multiSourceObject.writeLatestDataIntoDB(multiSourceObject.bureauEnergyM, 
    #                 sourceDataFolderName=bureauEnergyFolder, 
    #                 bureauSET=bureauSET())

    # end = timeCalculate()
    # print(f"{bureauEnergyFolder} 花費：", end-begin, "秒。")



    multiSourceObject.writeLatestDataIntoDB(multiSourceObject.ecommerceM,
                    sourceDataFolderName=pchomeFoler)
    end = timeCalculate()
    print(f"{pchomeFoler} 花費：", end-begin, "秒。")



    multiSourceObject.writeLatestDataIntoDB(multiSourceObject.ecommerceM, 
                    sourceDataFolderName=momoFolder)
    end = timeCalculate()
    print(f"{momoFolder} 花費：", end-begin, "秒。")













    # conn = engine.connect()

    # # result = conn.execute(f"select product_model from {tableClassBase.table2} where 3C_Id = {1}".format("1"))
    # Session = sessionmaker(bind=conn)
    # session = Session()

    # # rows = result.fetchall()
    # # print(rows[-5:])

    # result = pchome.getReferenceTupleFromDB(tableClassBase,session, "1")
    
    # print(result[-100:])

    # session.close()
    # conn.close()