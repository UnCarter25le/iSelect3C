# -*- coding:utf-8 -*-

"""
程式名稱： createForTablesAndDB.py
程式描述：


備　　註：

    

"""
import os
import sys
import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base

_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)

from libs.sqlDDLAndsqlAlchemyORM import (
                                        sqlDDLForTables,
                                        sqlORMForTables,
                                        rawSQLString,
                                        sqlObjectInitail
                                        )






if __name__ == '__main__':
    # must create a database in advance:
    #create database iSelect3C CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

    sqlDDL = sqlObjectInitail()._sqlDDL
    tableClassBase = sqlObjectInitail()._tableClassBase
    
    engine = tableClassBase.connectToMySQLEngine()


    # transaction 似乎只對DML有用。
    conn = engine.connect()
    trans = conn.begin()
    
    try:
        conn.execute("SET foreign_key_checks = 0")
        for table in sqlDDL.getTables():
            conn.execute(f"DROP TABLE if exists {table}")
        
        # 使用raw sqlString創建----------------------
        # for syn in sqlDDL.getMySQLSyntax():
        #     conn.execute(syn)

        # 利用 ORM 建立所有class資料表！----------------------
        tableClassBase._Base.metadata.create_all(conn)
        for key in iter(rawSQLString().MySQLAlterUniqueRawStringDict):
            alterSQLString = rawSQLString().MySQLAlterUniqueRawStringDict[key]
            if alterSQLString:
                conn.execute(alterSQLString)
        
    except (sqla.exc.InternalError, sqla.exc.ProgrammingError, sqla.exc.IntegrityError) as e:
        trans.rollback()
        # conn.rollback()  # AttribueError
        print()
        print("error code:", e)
        raise
    else:
        print("establish table:\n", "\n".join([t for t in tableClassBase.getTables()]))
    finally:
        conn.execute("SET foreign_key_checks = 1")
        trans.close()
        conn.close()
    