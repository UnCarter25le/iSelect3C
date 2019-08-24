# -*- coding:utf-8 -*-

"""
程式名稱： insertDataIntoDB.py
程式描述：


備　　註：

    

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
                                        bureauEnergyMunging
                                        )
from libs.timeWidget import timeCalculate
from libs.munging import bureauEnergyMunging as BureaurSET

if __name__ == '__main__':
    tableClassBase = sqlObjectInitail()._tableClassBase
    engine = tableClassBase.connectToMySQLEngine()

    


    referenceFiles().writeReferenceDataIntoDB(tableClassBase, engine)


    # begin = timeCalculate()
    # readyFile = os.listdir(f"{_BASE_PATH}/dataMunging/cleanData/bureauEnergy/")
    # readyFile.sort(key= lambda x: x.split('_')[1])
    # print()
    # print(readyFile[-12:])
    # for reFile in readyFile[-12:]:
    #     with open(f"{_BASE_PATH}/dataMunging/cleanData/bureauEnergy/{reFile}")as f:
    #         cleanFile = json.load(f)
    #     cleanFile["product"], setNums = BureaurSET().bureauDataProcessToSet(cleanFile["product"])
    #     bureauEnergyMunging().writeDataIntoDB(cleanFile)


    # end = timeCalculate()

    # print(end-begin)

