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

from libs.sqlDDLAndsqlAlchemyORM import sqlDDLForTables
from libs.sqlDDLAndsqlAlchemyORM import iSelect3CTableClasses





if __name__ == '__main__':
    # must create a database in advance:
    #create database iSelect3C CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

    sqlDDL = sqlDDLForTables("iSelect3C", 
                    table1="classes_of_consumer_electronics",
                    table2="bureau_energy_products",
                    table3="ecommerce",
                    table4="ecommerce_products",
                    table5="news_keywords",
                    table6="news_title_from_selenium",
                    table7="publishers_mapping",
                    table8="selected_news_with_tfidf",
                    table9="administrative_divisions_of_Taiwan",
                    table10="observation_stations",
                    table11="weather_records_by_months")
    tableClassBase = iSelect3CTableClasses("iSelect3C", 
                    table1="classes_of_consumer_electronics",
                    table2="bureau_energy_products",
                    table3="ecommerce",
                    table4="ecommerce_products",
                    table5="news_keywords",
                    table6="news_title_from_selenium",
                    table7="publishers_mapping",
                    table8="selected_news_with_tfidf",
                    table9="administrative_divisions_of_Taiwan",
                    table10="observation_stations",
                    table11="weather_records_by_months")

    # pymysql:
    # conn = pymysql.connect(sqlDDL._localhost, user=sqlDDL._databaseInitial__userLocal, passwd=sqlDDL._databaseInitial__passwdLocal, 
    #                         port=sqlDDL._port, 
    #                         db=sqlDDL.databaseName, charset=sqlDDL._charset)
    
    engine = sqla.create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset={5}".format(
                                                                                    sqlDDL._databaseInitial__userLocal, 
                                                                                    sqlDDL._databaseInitial__passwdLocal, 
                                                                                    sqlDDL._localhost, 
                                                                                    sqlDDL._port, 
                                                                                    sqlDDL.databaseName, 
                                                                                    sqlDDL._charset))
    # transaction 似乎只對DML有用。
    conn = engine.connect()
    trans = conn.begin()
    
    try:
        conn.execute("SET foreign_key_checks = 0")
        for table in sqlDDL.getTables():
            conn.execute(f"DROP TABLE if exists {table}")
        
        # for syn in sqlDDL.getMySQLSyntax():
        #     conn.execute(syn)
        # 利用 ORM 建立所有class資料表！
        tableClassBase._Base.metadata.create_all(conn)
        # conn.execute(tableClassBase.bureauEnergyProducts().series_Id)
        
    except (sqla.exc.InternalError, sqla.exc.ProgrammingError, sqla.exc.IntegrityError) as e:
        trans.rollback()
        print()
        print("error code:", e)
        raise
    else:
        print("establish table:", sqlDDL.getTables())
    finally:
        conn.execute("SET foreign_key_checks = 1")
        trans.close()
        conn.close()
    