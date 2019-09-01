# -*- coding:utf-8 -*-

"""
程式名稱： createForTablesAndDB.py
程式描述：


備　　註：

    

https://gist.github.com/absent1706/3ccc1722ea3ca23a5cf54821dbc813fb
https://myapollo.com.tw/2019/08/04/sqlalchemy-truncate-tables/
參考資料表的truncate
        


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
                                        sqlObjectInitial
                                        )
from libs.sqlDMLAndsqlAlchemyORM import writeDataWhenMunging






if __name__ == '__main__':
    # must create a database in advance:
    #create database iSelect3C CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

    sqlDDL = sqlObjectInitial._sqlDDL
    
    """
    在 sqlDMLAndsqlAlchemyORM 的 class writeDataWhenMunging(referenceFiles): 
    選擇 tableClassBase
    
    """
    tableClassBase = writeDataWhenMunging._tableClassBase
    
    engine = sqlObjectInitial.loadCorrectEngine(tableClassBase, tableClassBase.databaseName)
    

    # transaction 似乎只對DML有用。
    conn = engine.connect()
    trans = conn.begin()

    foreignKeyClose, foreignKeyOpen = sqlObjectInitial.loadCorrectForeignKeyConstraintSet(tableClassBase.databaseName)
    
    print(foreignKeyClose, foreignKeyOpen)
    try:
        conn.execute(f"{foreignKeyClose}")

        

        #------------------------------------------------------------------------------------------

        # 使用raw sqlstring drop tables
        # for table in sqlDDL.getTables():
        #     conn.execute(f"DROP TABLE if exists {table}")


        # 使用ORM 清空所有表格資料  <class 'sqlalchemy.sql.schema.Table'>
        # 綁定引擎的MetaData，等於是資料庫的元資料，可以用來操控資料表class。
        # MetaData = sqla.MetaData(bind=engine, reflect=True) 
        # --->MetaData(bind=Engine(mysql+pymysql://root:***@localhost:3306/iSelect3C?charset=utf8mb4))
        # trans = conn.begin() 
        # for table in MetaData.sorted_tables:
            # print(table)
        #     conn.execute(table.delete())
        # trans.commit()
        
        #------------------------------------------------------------------------------------------

        # 叫出所有表格名稱（字串）# 因為所有的class都繼承 Base，因此用Base呼叫metadata元資料方法，可以叫出表格的名稱。
        # for t in tableClassBase._Base.metadata.tables:  # 
        #     if t == "weather_records_by_months":
        #         print(1)
        #     print(type(t))

        #------------------------------------------------------------------------------------------


        # 使用raw sqlString創建----------------------
        # for syn in sqlDDL.getMySQLSyntax():
        #     conn.execute(syn)

        # # 利用 ORM 建立所有class資料表！----------------------若只想單獨重建表格「news_title_from_selenium」，則需要將相關聯的表格一起drop，才能重建。不想要同時重建的表格，必須註解。
        # tableClassBase._Base.metadata.create_all(conn)
        # for key in iter(rawSQLString().MySQLAlterUniqueRawStringDict):
        #     alterSQLString = rawSQLString().MySQLAlterUniqueRawStringDict[key]
        #     if alterSQLString:
        #         conn.execute(alterSQLString)

        
        
        
    except (sqla.exc.InternalError, sqla.exc.ProgrammingError, sqla.exc.IntegrityError) as e:
        trans.rollback()
        # conn.rollback()  # AttribueError
        print()
        print("error code:", e)
        raise
    else:
        print("establish table:\n", "\n".join([t for t in tableClassBase.getTables()]))
    finally:
        conn.execute(f"{foreignKeyOpen}")
        trans.close()
        conn.close()
    