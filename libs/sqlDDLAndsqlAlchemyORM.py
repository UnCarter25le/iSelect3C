# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。

import os
import sys
# import datetime
import sqlalchemy as sqla
from sqlalchemy import (
                         Column,
                         ForeignKey,
                         PrimaryKeyConstraint,
                         ForeignKeyConstraint
                         )
from sqlalchemy.orm import column_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import (
                                        TINYINT,
                                        SMALLINT,
                                        NVARCHAR,
                                        VARCHAR,
                                        CHAR,
                                        MEDIUMINT,
                                        INTEGER,
                                        DECIMAL,
                                        FLOAT,
                                        DATE,
                                        DATETIME,
                                        JSON
                                   )


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

class rawSQLString(object):

     MySQLRawStringDict = {"classes_of_consumer_electronics":"""
                                                  CREATE TABLE classes_of_consumer_electronics(
                                                       3C_Id tinyint UNSIGNED PRIMARY KEY,
                                                       product nvarchar(10) Not Null default "None",
                                                       uri_of_bureau_energy varchar(230) Not Null default "None",
                                                       uri_of_momo varchar(210) Not Null default "None",
                                                       uri_of_pchome varchar(90) Not Null default "None"
                                                  )""",
                    "bureau_energy_products":"""
                                                  CREATE TABLE bureau_energy_products(
                                                       product_model nvarchar(35) PRIMARY KEY,
                                                       3C_Id tinyint UNSIGNED  Not Null,
                                                       series_Id mediumint UNSIGNED  UNIQUE KEY AUTO_INCREMENT,
                                                       bureau_product_Id char(6) Not Null default "None",
                                                       brand_name nvarchar(50) Not Null default "None",
                                                       login_number varchar(15) Not Null default "None",
                                                       detail_uri varchar(250) Not Null default "None",
                                                       labeling_company nvarchar(20) Not Null default "None",
                                                       efficiency_rating char(1) Not Null default "N",
                                                       from_date_of_expiration date Not Null default "1970-01-01",
                                                       energy_efficiency_label_outer_uri varchar(100) Not Null default "None",
                                                       energy_efficiency_label_inner_uri nvarchar(120) Not Null default "None",
                                                       test_report_of_energy_efficiency JSON default null,
                                                       efficiency_benchmark varchar(15) Not Null default "None",
                                                       annual_power_consumption_degrees_dive_year varchar(4) Not Null default "None",

                                                       Constraint classes_of_consumer_electronics2bureau_energy_products foreign key(3C_Id)
                                                       references classes_of_consumer_electronics(3C_Id) 
                                                       ON UPDATE CASCADE ON DELETE CASCADE
                                                  )
                                                  """,
                    "ecommerce":"""
                                                  CREATE TABLE ecommerce(
                                                       ecommerce_Id tinyint UNSIGNED PRIMARY KEY,
                                                       en_name varchar(8) Not Null default "None",
                                                       ch_name nvarchar(10) Not Null default "None"
                                                  )""",
                    "ecommerce_products":"""
                                                  CREATE TABLE ecommerce_products(
                                                       ecommerce_product_Id varchar(20) PRIMARY KEY,
                                                       ecommerce_Id tinyint UNSIGNED  Not Null, 
                                                       series_Id int UNSIGNED UNIQUE KEY AUTO_INCREMENT,
                                                       name nvarchar(80) Not Null default "None",
                                                       originprice varchar(7) Not Null default "None",
                                                       pics varchar(70) Not Null default "None",
                                                       picb varchar(70) Not Null default "None",
                                                       produrl varchar(55) Not Null default "None",

                                                       Constraint ecommerce2ecommerce_products foreign key(ecommerce_Id)
                                                       references ecommerce(ecommerce_Id)
                                                       ON UPDATE CASCADE ON DELETE CASCADE
                                                  )""",
                    "news_keywords":"""
                                                  CREATE TABLE news_keywords(
                                                       news_key_Id tinyint UNSIGNED PRIMARY KEY,
                                                       keyword nvarchar(6) Not Null default "None"
                                                  )""",
                    "news_title_from_selenium":"""
                                                  CREATE TABLE news_title_from_selenium(
                                                       news_title_Id mediumint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                                       news_key_Id tinyint UNSIGNED Not Null,
                                                       news_url varchar(270) Not Null default "None",
                                                       news_title nvarchar(50) Not Null default "None",
                                                       publisher nvarchar(9) Not Null default "None",
                                                       publish_date date Not Null default "1970-01-01",
                                                       ctime datetime Not Null default "1970-01-01 00:00:00",

                                                       Constraint news_keywords2news_title_from_selenium foreign key(news_key_Id)
                                                       references news_keywords(news_key_Id)
                                                       ON UPDATE CASCADE ON DELETE CASCADE
                                                  )""",
                    "publishers_mapping":"""
                                                  CREATE TABLE publishers_mapping(
                                                       publisher_Id tinyint UNSIGNED PRIMARY KEY,
                                                       publisher nvarchar(9) Not Null default "None"
                                                  )""",
                    "selected_news_with_tfidf":"""
                                                  CREATE TABLE selected_news_with_tfidf(
                                                       news_title_Id mediumint UNSIGNED PRIMARY KEY,
                                                       series_Id mediumint UNSIGNED UNIQUE KEY AUTO_INCREMENT ,
                                                       publisher_Id tinyint UNSIGNED Not Null,
                                                       news_content nvarchar(2000) Not Null default "None",
                                                       
                                                       Constraint publishers_mapping2selected_news_with_tfidf foreign key(publisher_Id)
                                                       references publishers_mapping(publisher_Id)
                                                       ON UPDATE CASCADE ON DELETE CASCADE,

                                                       Constraint news_title_from_selenium2selected_news_with_tfidf foreign key(news_title_Id)
                                                       references news_title_from_selenium(news_title_Id)
                                                       ON UPDATE CASCADE ON DELETE CASCADE
                                                  )""",
                    "administrative_divisions_of_Taiwan":"""
                                                  CREATE TABLE administrative_divisions_of_Taiwan(
                                                       division_Id tinyint UNSIGNED PRIMARY KEY,
                                                       ch_name nchar(3) Not Null default "N",
                                                       en_name varchar(20) Not Null default "None",
                                                       code_name char(3) Not Null default "N"
                                                  )""",
                    "observation_stations":"""
                                                  CREATE TABLE observation_stations(
                                                       station_Id char(6) PRIMARY KEY,
                                                       division_Id tinyint UNSIGNED Not Null,
                                                       series_Id smallint UNSIGNED UNIQUE KEY AUTO_INCREMENT,
                                                       ch_name nvarchar(10) Not Null default "None",
                                                       en_name varchar(30) Not Null default "None",
                                                       number_of_station char(1) Not Null default "N",

                                                       Constraint administrative_divisions_of_Taiwan2observation_stations foreign key(division_Id)
                                                       references administrative_divisions_of_Taiwan(division_Id)
                                                       ON UPDATE CASCADE ON DELETE CASCADE

                                                  )""",
                    "weather_records_by_months":"""
                                                  CREATE TABLE weather_records_by_months(
                                                       record_Id char(13) PRIMARY KEY,
                                                       station_Id char(6) Not Null,
                                                       temperature_average decimal(3,1) Not Null default 0.0,
                                                       temperature_high decimal(3,1) Not Null default 0.0,
                                                       temperature_high_date date Not Null default "1970-01-01",
                                                       temperature_low decimal(3,1) Not Null default 0.0,
                                                       temperature_low_date date Not Null default "1970-01-01",
                                                       relative_humidity_average tinyint UNSIGNED Not Null default 0,
                                                       relative_humidity_low tinyint UNSIGNED Not Null default 0,
                                                       relative_humidity_low_date date Not Null default "1970-01-01",
                                                       rainful decimal(5,1) Not Null default 0.0,
                                                       raining_days tinyint UNSIGNED Not Null default 0,

                                                       Constraint observation_stations2weather_records_by_months foreign key(station_Id)
                                                       references observation_stations(station_Id)
                                                       ON UPDATE CASCADE ON DELETE CASCADE
                                                  )""",
                    "None":""
     }

     
class databaseInitial(object):
    
     __userLocal = "root"
     __passwdLocal = "admin"
     _port = 3306
     _charset = "utf8mb4"
     _localhost = "localhost"

     def __init__(self, databaseName, **kwargs):
          self.databaseName = databaseName
          self.table1 = kwargs.get("table1", "None")
          self.table2 = kwargs.get("table2", "None")
          self.table3 = kwargs.get("table3", "None")
          self.table4 = kwargs.get("table4", "None")
          self.table5 = kwargs.get("table5", "None")
          self.table6 = kwargs.get("table6", "None")
          self.table7 = kwargs.get("table7", "None")
          self.table8 = kwargs.get("table8", "None")
          self.table9 = kwargs.get("table9", "None")
          self.table10 = kwargs.get("table10", "None")
          self.table11 = kwargs.get("table11", "None")
          self.table12 = kwargs.get("table12", "None")
          
          self.tableList = [self.table1, self.table2, self.table3, self.table4, self.table5,
                         self.table6, self.table7, self.table8, self.table9, self.table10, 
                         self.table11, self.table12]

     def getTables(self):

          return [t for t in self.tableList if t != "None"]
    
     def __str__(self):
          return f"""
          連結資料庫：{self.databaseName},
          表格：{self.table1} & 
               {self.table2} & 
               {self.table3} & 
               {self.table4} & 
               {self.table5} &
               {self.table6} & 
               {self.table7} & 
               {self.table8} & 
               {self.table9} & 
               {self.table10} &
               {self.table11} & 
               {self.table12}"""

     # def __repr__(self):
     #      return f"""
     #      連結資料庫：{self.databaseName},
     #      表格：{self.table1} &"""


class sqlDDLForTables(databaseInitial):
    # self取屬性或方法的用法，只能在def裡面。
    # aaa = self.__str__()
     _MySQLRawStringDict = rawSQLString().MySQLRawStringDict

     def __init__(self, databaseName, **kwargs):
        # 使用super()來讓父類別幫忙做事¶
          super().__init__(databaseName, **kwargs) #除了self會派回去給父類不用寫外，父類的其他參數要填上
          
          
          self._MySQLTable1 = self._MySQLRawStringDict[self.table1]
          self._MySQLTable2 = self._MySQLRawStringDict[self.table2]
          self._MySQLTable3 = self._MySQLRawStringDict[self.table3]
          self._MySQLTable4 = self._MySQLRawStringDict[self.table4]
          self._MySQLTable5 = self._MySQLRawStringDict[self.table5]
          self._MySQLTable6 = self._MySQLRawStringDict[self.table6]
          self._MySQLTable7 = self._MySQLRawStringDict[self.table7]
          self._MySQLTable8 = self._MySQLRawStringDict[self.table8]
          self._MySQLTable9 = self._MySQLRawStringDict[self.table9]
          self._MySQLTable10 = self._MySQLRawStringDict[self.table10]
          self._MySQLTable11 = self._MySQLRawStringDict[self.table11]
          self._MySQLTable12 = self._MySQLRawStringDict[self.table12]

          self._MySQLSyntaxList = [self._MySQLTable1, self._MySQLTable2, self._MySQLTable3,  self._MySQLTable4,  self._MySQLTable5,
                                   self._MySQLTable6,  self._MySQLTable7,  self._MySQLTable8,  self._MySQLTable9,  self._MySQLTable10,
                                   self._MySQLTable11, self._MySQLTable12]
    
     def getMySQLSyntax(self):

          return [syn for syn in self._MySQLSyntaxList if syn]
        
cc = sqlDDLForTables("iSelect3C",
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


# print(cc)
# print(len(cc.getMySQLSyntax()))
# for row in cc.getMySQLSyntax():
#     print(row.split("\n")[1])



class iSelect3CTableClasses(databaseInitial):
     """
     https://docs.sqlalchemy.org/en/13/faq/ormconfiguration.html?highlight=foreign%20key
     column_property(Column(Integer, primary_key=True), A.id)  借用其他class欄位的既有屬性

     https://docs.sqlalchemy.org/en/13/orm/join_conditions.html?highlight=foreign%20key
     __table_args__  外部表格的主鍵為本表的外部鍵時，將此外部鍵同設為主鍵
     
     http://seasell2.blogspot.com/2013/07/sql-foreign-key.html
     https://docs.sqlalchemy.org/en/13/core/constraints.html?highlight=foreign%20key
     onupdate - Typical values include CASCADE, DELETE and RESTRICT , SET NULL.
     ondelete - Typical values include CASCADE, DELETE and RESTRICT , SET NULL.

     https://docs.sqlalchemy.org/en/13/orm/persistence_techniques.html?highlight=default%20value
     default值的kwargs，建議以server_default


     https://stackoverflow.com/questions/19243232/sqlalchemy-how-to-make-an-integer-column-auto-increment-and-unique-without-ma
     how to set unique key autoincrement in sqlalchemy?
     Can not! Just abide by the following command-line after base-up all classes:
     "ALTER TABLE `bureau_energy_products` ADD `series_Id` mediumint UNSIGNED Not Null AUTO_INCREMENT, ADD UNIQUE (`series_Id`);"

     https://stackoverflow.com/questions/32959336/how-to-insert-null-value-in-sqlalchemy
     python的 None 就等於 mysql column's Null


     """
     

      # _Base 意思類似 django的models.Model
     _Base = declarative_base()



     def getAlterUniqueSyntax(self):

          bureau_energy_products_series_Id = "ALTER TABLE `bureau_energy_products` modify `series_Id` mediumint UNSIGNED Not Null AUTO_INCREMENT, ADD UNIQUE (`series_Id`);"
          return bureau_energy_products_series_Id

     # class Zoo(_Base):

     #      __tablename__ = "zoo"
     #      # critter = Column("critter", NVARCHAR(length=20),primary_key=True)
     #      critter = Column("critter", NVARCHAR(length=20))
     #      count = Column("count", SMALLINT(unsigned=True), nullable=False, server_default="56")
     #      damages = Column("damages", FLOAT, nullable=False, server_default="56.0")
          
     #      def __init__(self, critter, count, damages):
     #           self.critter = critter
     #           self.count = count
     #           self.damages = damages

     #      def __str__(self):
     #           return "<Zoo({}, {}, {})>".format(self.critter, self.count, self.damages)

     #      # table_args裡面單一元素的話，必須加「,」； autoincrement不能加在這裡
     #      __table_args__ = (

     #           PrimaryKeyConstraint("critter"),

     #      )

     # class Zoo2(Zoo):
          
     #      __tablename__ = "zoo2"
     #      id = Column("id")
     #      # f_id = Column(ForeignKey("zoo.critter", onupdate="CASCADE", ondelete="SET NULL"),  primary_key=True) # 這邊的primary_key設定無效
          
     #      __table_args__ = (
     #           # constraint的用法當是「統一宣告多個鍵」，不用此法的話，就每個欄位宣告
     #           PrimaryKeyConstraint('id'),
     #           ForeignKeyConstraint(
     #                ['id'],
     #                ['zoo.critter'],
     #                name = "PKandFKsimaltaniously",
     #                onupdate="CASCADE", ondelete="CASCADE"
     #           )
     #      )
          

          
     
     class classesOfConsumerElectronics(_Base):
          __tablename__ = "classes_of_consumer_electronics"
          Id_3C = Column("3C_Id", TINYINT(unsigned=True), autoincrement=False) #  primary_key=True
          product = Column("product", NVARCHAR(length=10), nullable=False, server_default="None")
          uri_of_bureau_energy = Column("uri_of_bureau_energy", VARCHAR(length=230), nullable=False, server_default="None")
          uri_of_momo = Column("uri_of_momo", VARCHAR(length=210), nullable=False, server_default="None")
          uri_of_pchome = Column("uri_of_pchome", VARCHAR(length=90), nullable=False, server_default="None")

          __table_args__ = (

               PrimaryKeyConstraint("3C_Id"),

          )

          def __init__(self, Id_3C, product, uri_of_bureau_energy, uri_of_momo, uri_of_pchome):
               self.Id_3C = Id_3C
               self.product = product
               self.uri_of_bureau_energy = uri_of_bureau_energy
               self.uri_of_momo = uri_of_momo
               self.uri_of_pchome = uri_of_pchome

     class bureauEnergyProducts(_Base):

          __tablename__ = "bureau_energy_products"
          product_model = Column("product_model", NVARCHAR(length=35), autoincrement=False)
          Id_3C = Column("3C_Id", nullable=False)
          # unique key can not be set up with autoincrement!
          series_Id = Column("series_Id", MEDIUMINT(unsigned=True), autoincrement=True, unique=True)
          bureau_product_Id = Column("bureau_product_Id", CHAR(length=6), nullable=False, server_default="None")
          brand_name = Column("brand_name", NVARCHAR(length=50), nullable=False, server_default="None")
          login_number = Column("login_number", VARCHAR(length=15), nullable=False, server_default="None")
          detail_uri = Column("detail_uri", VARCHAR(length=250), nullable=False, server_default="None")
          labeling_company = Column("labeling_company", NVARCHAR(length=20), nullable=False, server_default="None")
          efficiency_rating = Column("efficiency_rating", CHAR(length=1), nullable=False, server_default="N")
          from_date_of_expiration = Column("from_date_of_expiration", DATE, nullable=False, server_default="1970-01-01")
          energy_efficiency_label_outer_uri = Column("energy_efficiency_label_outer_uri", VARCHAR(length=100), nullable=False, server_default="None")
          energy_efficiency_label_inner_uri = Column("energy_efficiency_label_inner_uri", NVARCHAR(length=120), nullable=False, server_default="None")
          test_report_of_energy_efficiency = Column("test_report_of_energy_efficiency", JSON, nullable=False, server_default=None)
          efficiency_benchmark = Column("efficiency_benchmark", VARCHAR(length=15), nullable=False, server_default="None")
          annual_power_consumption_degrees_dive_year = Column("annual_power_consumption_degrees_dive_year", VARCHAR(length=4), nullable=False, server_default="None")
          # = Column("", VARCHAR(length=),nullable=False, server_default="None")

          __table_args__ = (
               PrimaryKeyConstraint("product_model"),
               ForeignKeyConstraint(
                    ["3C_Id"], ["classes_of_consumer_electronics.3C_Id"],
                    name="classes_of_consumer_electronics2bureau_energy_products",
                    onupdate="CASCADE", ondelete="CASCADE"
               )

          )

          def __init__(self, product_model, Id_3C, series_Id, bureau_product_Id, brand_name,
                    login_number, detail_uri, labeling_company, efficiency_rating, from_date_of_expiration,
                    energy_efficiency_label_outer_uri, energy_efficiency_label_inner_uri, test_report_of_energy_efficiency,
                    efficiency_benchmark, annual_power_consumption_degrees_dive_year):
               self.product_model = product_model
               self.Id_3C = Id_3C
               self.series_Id = series_Id
               self.bureau_product_Id = bureau_product_Id
               self.brand_name = brand_name
               self.login_number = login_number
               self.detail_uri = detail_uri
               self.labeling_company = labeling_company
               self.efficiency_rating = efficiency_rating
               self.from_date_of_expiration = from_date_of_expiration
               self.energy_efficiency_label_outer_uri = energy_efficiency_label_outer_uri
               self.energy_efficiency_label_inner_uri = energy_efficiency_label_inner_uri
               self.test_report_of_energy_efficiency = test_report_of_energy_efficiency
               self.efficiency_benchmark = efficiency_benchmark
               self.annual_power_consumption_degrees_dive_year = annual_power_consumption_degrees_dive_year
               

     class ecommerce(_Base):
          __tablename__ = "ecommerce"
          ecommerce_Id = Column("ecommerce_Id", TINYINT(unsigned=True), autoincrement=False)
          en_name = Column("en_name", VARCHAR(length=8), nullable=False, server_default="None")
          ch_name = Column("ch_name", NVARCHAR(length=10), nullable=False, server_default="None")

          __table_args__ = (
               PrimaryKeyConstraint("ecommerce_Id"),
          )
          def __init__(self, ecommerce_Id, en_name,ch_name):
               self.ecommerce_Id = ecommerce_Id
               self.en_name = en_name
               self.ch_name = ch_name
     
     
     # class (_Base):
     #      __tablename__ = ""
     #      = Column("", VARCHAR(length=), autoincrement=False)
     #      = Column("", VARCHAR(length=), nullable=False, server_default="None")
     #      __table_args__ = (
     #           PrimaryKeyConstraint("product_model"),
     #           ForeignKeyConstraint(
                    
     #           ) 

     #      )
     #      def __init__(self,,,,):
     #           self. = 
     #           self. = 
     #           self. = 


          # class (_Base):
     #      __tablename__ = ""
     #      = Column("", VARCHAR(length=), autoincrement=False)
     #      = Column("", VARCHAR(length=), nullable=False, server_default="None")
     #      __table_args__ = (
     #           PrimaryKeyConstraint("product_model"),
     #           ForeignKeyConstraint(
                    
     #           ) 

     #      )
     #      def __init__(self,,,,):
     #           self. = 
     #           self. = 
     #           self. = 


          # class (_Base):
     #      __tablename__ = ""
     #      = Column("", VARCHAR(length=), autoincrement=False)
     #      = Column("", VARCHAR(length=), nullable=False, server_default="None")
     #      __table_args__ = (
     #           PrimaryKeyConstraint("product_model"),
     #           ForeignKeyConstraint(
                    
     #           ) 

     #      )
     #      def __init__(self,,,,):
     #           self. = 
     #           self. = 
     #           self. = 


          # class (_Base):
     #      __tablename__ = ""
     #      = Column("", VARCHAR(length=), autoincrement=False)
     #      = Column("", VARCHAR(length=), nullable=False, server_default="None")
     #      __table_args__ = (
     #           PrimaryKeyConstraint("product_model"),
     #           ForeignKeyConstraint(
                    
     #           ) 

     #      )
     #      def __init__(self,,,,):
     #           self. = 
     #           self. = 
     #           self. = 


          # class (_Base):
     #      __tablename__ = ""
     #      = Column("", VARCHAR(length=), autoincrement=False)
     #      = Column("", VARCHAR(length=), nullable=False, server_default="None")
     #      __table_args__ = (
     #           PrimaryKeyConstraint("product_model"),
     #           ForeignKeyConstraint(
                    
     #           ) 

     #      )
     #      def __init__(self,,,,):
     #           self. = 
     #           self. = 
     #           self. = 


          # class (_Base):
     #      __tablename__ = ""
     #      = Column("", VARCHAR(length=), autoincrement=False)
     #      = Column("", VARCHAR(length=), nullable=False, server_default="None")
     #      __table_args__ = (
     #           PrimaryKeyConstraint("product_model"),
     #           ForeignKeyConstraint(
                    
     #           ) 

     #      )
     #      def __init__(self,,,,):
     #           self. = 
     #           self. = 
     #           self. = 


          # class (_Base):
     #      __tablename__ = ""
     #      = Column("", VARCHAR(length=), autoincrement=False)
     #      = Column("", VARCHAR(length=), nullable=False, server_default="None")
     #      __table_args__ = (
     #           PrimaryKeyConstraint("product_model"),
     #           ForeignKeyConstraint(
                    
     #           ) 

     #      )
     #      def __init__(self,,,,):
     #           self. = 
     #           self. = 
     #           self. = 


          # class (_Base):
     #      __tablename__ = ""
     #      = Column("", VARCHAR(length=), autoincrement=False)
     #      = Column("", VARCHAR(length=), nullable=False, server_default="None")
     #      __table_args__ = (
     #           PrimaryKeyConstraint("product_model"),
     #           ForeignKeyConstraint(
                    
     #           ) 

     #      )
     #      def __init__(self,,,,):
     #           self. = 
     #           self. = 
     #           self. = 
          

     






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

print(tableClassBase.getAlterUniqueSyntax())
