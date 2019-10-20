
# Preface
## "iSelect3C" is the project powered by Tom, JiaSyuan, and I(Carter).
- The project was created for OPEN DATA Innovative Application Contest, which was hosted by several Government Departments on 2019 May.
- The project's intention is to reduce the information gap between consumers and sellers, especially when a consumer is eaget to puchase energy-saving consumer electronics which's certification is within the validity period. 
- In addtion, we offer simple but comprehensive calculator to leave users to have better understanding of something worthwhile to watch, such as what possible eletronic fees is and how it cost under the official specifications provided by Bureau of Energy of of Ministry of Economic Affairs.
- The mvp website is " http://herbmagicwebapi.azurewebsites.net/iselect3C " , and we all know that is not enough to see it as an mature web application. But still, it has enabled users to pick out the products that are validated by government from e-commerce, pchome and momo.

- The powerpoint file's link: https://www.evernote.com/shard/s379/sh/4b48b19f-b712-4353-80c3-44995f91956d/9cac2778c89f5f4b61aa1398921f00dc  .
--------
--------
--------

# These section are the zone of development. 

## 1. Environment:
- python 3.6.8
- Packages my environment installed and it can be found in `requirements.txt`.

```
autopep8==1.4.4
beautifulsoup4==4.7.1
certifi==2019.3.9
chardet==3.0.4
idna==2.8
jieba==0.39
pycodestyle==2.5.0
pymssql==2.1.1
PyMySQL==0.9.3
requests==2.22.0
selenium==3.141.0
six==1.12.0
soupsieve==1.9.1
splinter==0.10.0
SQLAlchemy==1.3.7
urllib3==1.25.3
lxml==4.4.1
pip==19.2.3
setuptools==41.0.1
wheel==0.33.4


Hignly recommend holding the version of pymssql at 2.1.1.
```


## 2. The structure of my contribution(data acquisition and munging):

```
/cralwer/
    |___pchomeApi.py______________________> Crawling date in one main process way via api.
    |___pchomeApiMulti.py_________________> Crawling date in a multiprocess manner via api.
    |___momoMulti.py______________________> Crawling date in a multiprocess(selenium) manner. 
    |                                       Noting that it must kill chrome process 
    |                                       mannally after executing this program.
    |___bureauEnergyMulti_1.py____________> Crawling date in a multiprocess manner from official web site.
    |___bureauEnergyMulti_2.py____________> Crawling date in a multiprocess manner.
    |___googleNews.py_____________________> Crawling data in one main process way(selenium) from search result page.
    |___googleNewsMulti.py________________> Crawling data in a multiprocess(selenium) manner from search result page.
    |___weatherObservationStation.py______> Crawling data in one main process way(selenium) from official web site.
    |___weatherRecordMulti.py_____________> Crawling date in a multiprocess manner from official web site.
    |___selectedNewsMulti.py______________> Crawling date in a multiprocess manner from a few select news Url.

/database/
    |___referenceJSON_____________________> offering the reference foreign mapping when writing data into DB.
    |           |___administrative_divisions_of_Taiwan.json
    |           |___classes_of_consumer_electronics.json
    |           |___ecommerce.json
    |           |___news_keywords.json
    |           |___publishers_mapping.json
    |           |___many other you name it.
    |           
    |___createForTablesAndDB.py____________> using SQLAlchemy ORM ro raw SQL string to create tables.
    |___insertLatestDataIntoDB.py__________> write last data set into DB, such as bureau, ecommerce and so on.
    |___insertHistoricalDataIntoDB.py______> write historical data set, known as local one, into DB.
    

/dataMunging/
    |___pchomeMunging.py__________________> Munging date, json format, after having raw data in 
    |                                       "/rawData/pchome/冷暖空調/「24h」「kdn」「vdr」".
    |___momoMunging.py____________________> Munging date, text format, after having raw data in 
    |                                       "/rawData/momo/「冷暖空調」「電冰箱」「除濕機」..., and you name it".
    |___bureauEnergyMunging.py____________> Munging date, text format, after having raw data in
    |                                       "/rawData/bureauEnergy/「冷暖空調」「電冰箱」「除濕機」..., and you name   
    |                                       it".
    |
    |___observationStationMunging.py______> Munging data, text format, after having raw data in 
    |                                       "/rawData/observationStation/overviewData/".
    |
    |___newsMunging.py____________________> Munging data, json format, after having raw data in 
    |                                       "/rawData/news/google/「家電促銷」「家電汰舊換新」「家電節能補助」..., 
    |                                       and you name it".
    |
    |
    |___cleanData/_ _ _ _ __ _ _ _ _ _ _ _> storing the data, json format, which is ready for inserting into DB.
    |       |___bureauEnergy/
    |       |___momo/
    |       |___news/
    |       |___newsWithContent/
    |       |___weather/
    |       |___observationStation/
    |       |___pchome/
    |
    |___rawData/_ _ _ _ __ _ _ _ __ _ _ _ > storing the data, json or text format, which is ready for munging 
            |                               into json files.
            |___bureauEnergy/
            |       |___無風管空氣調節機/
            |       |       |___overview/
            |       |       |   |___1_797_無風管空氣調節機.txt
            |       |       |   |___many other you name it.
            |       |       |___deatil/
            |       |       |   |___1_7964_無風管空氣調節機.txt
            |       |       |   |___many other you name it.
            |       |       |  
            |       |       |___jsonIntegration/
            |       |           |___bureauEnergy_detail_2019-06-24-16-09_7964_無風管空氣調節機.json
            |       |           |___bureauEnergy_overview_2019-06-24-16-09_7964_無風管空氣調節機.json
            |       |___ many other you name it. Already have all categories of consumer electronics!
            |
            |___momo/
            |   |___badRequest/
            |   |___冷暖空調/
            |   |   |___1_67_冷暖空調.txt
            |   |   |___many other you name it.
            |   |___ many other you name it.
            |
            |___pchome/
            |   |___badRequest/
            |   |___冷暖空調/
            |           |___ 24h/
            |           |   |___1_62_1233_24h冷暖空調.json
            |           |   |___many other you name it.
            |           |___ kdn/
            |           |___ vdr/
            |
            |___weather/
            |   |___2009/
            |   |   |___1_2009.txt
            |   |   |___many other you name it.
            |   |___many other you name it.
            |   
            |___observationStation/
            |   |___overviewData/
            |       |___observation_2019-06-10-17-13.txt
            |
            |___news/
            |   |___google/
            |   |   |___家電促銷/
            |   |   |       |___google_2019-06-22-00-42_216_家電促銷.json
            |   |   |___ many other you name it.
            |   |
            |   |___newsIntegration/
            |   |   |___news_2019-06-23-23-31_415_家電促銷^家電汰舊換新^家電節能補助.json
            ...
            ...
            ...
            more in the future!

/dataMining/
    |___dictionary/ (confidential)
    |   |___decision/ 
    |   |       |___testResultOfSelectedNewsUrl.txt
    |   |___jiebaCut_resultOfNewsTitle.json
    |   |___newsTitle_stop_words.txt
    |   |___newsTitle_wanted_words.txt
    |   |___TFIDF_resultOfNewsTitle.json
    |
    |___calculateForNewsPulisher.py_______> As for the integration of google news, gain the distribution 
    |                                       of news publisher.
    |___copewithNewsUrl.py________________> Extract the accurate and acceptable news Urls with reference to the
    |                                       result of TF-IDF.
    |___jiebaForNewsTitle.py______________> Produce the analysis result of TF-IDF from the integration of google news.


/libs/
    |___manipulateDir.py__________________> mkdir or rmdir whenever we wanna make crawling or munging.
    |___multiProcessing.py________________> Needed by programs those operations are in a mulitprocess manner.
    |___munging.py________________________> Needed by programs which are ready to process raw data.(confidential)
    |___minging.py________________________> Needed by programs which are ready to deal with text.(confidential)
    |___regex.py__________________________> Used in the situations in which we wanna extract accurate data type
    |                                       from raw data.(confidential)
    |___splinterBrowser.py________________> Used by programs which require chromdirver to start up browsers.
    |___timeWidget.py_____________________> Used when the interval peiod is needed in programs' processing.
    |___httpRequests.py___________________> Be imported while the useage of the fixed parameters.
    |___sqlDDLAndsqlAlchemyORM.py_________> Be imported while constructing database.(confidential)
    |___sqlDMLAndsqlAlchemyORM.py_________> Be imported while manipulating database.(confidential)



/doc/
    |___iSelect3C使用案例圖.png______________> Overview for use case diagram.
    |___iSelect3C活動圖.png_________________> Overview for activity diagram.
    |___chromedriver_______________________> according to: http://chromedriver.chromium.org/downloads
    |                                       editionInfo: ChromeDriver 75.0.3770.90
    |                                       execute `sudo cp chromedriver /usr/local/bin/`
    |___config_website.ini__________________> test file. (confidential)
    |___NOTE.md_____________________________> whole project note. (confidential)
    |___UML.asta____________________________> design of this project. (confidential)

/___
    |___README.md
    |___.gitignore
    |___requirements.txt____________________> Packages my environment installed.


```
- ### Note: Several files have been selected to be protected for concerns, and u are able to be notice about these signs by reading 「(confidential)」.

## 3. The process of executing the ".py" file:
> You are supposed to measure your machine's condition and `modify the numbers of processes` which are set in *multi.py while executing programs with multiprocess design.

- ### 3-1. pchome, the order of executing:

    ```
    pchomeApi.py  or  pchomeApiMulti.py  -->  pchomeMunging.py

    ```

- ### 3-2. momo, the order of executing:

    ```
    momoMulti.py   -->  momoMunging.py

    ```

- ### 3-3. bureauEnergy, the order of executing:

    ```
    bureauEnergyMulti_1.py  -->  bureauEnergyMulti_2.py  -->  bureauEnergyMunging.py

    ```
- ### 3-4. Central weather bureau, the order of executing:

    ```
    weatherRecordMulti.py  

    weatherObservationStation.py  -->  observationStationMunging.py

    ```

- ### 3-5. google news from specific keywords input, the order of executing:

    ```
    goodleNewsMulti.py  -->  newsMunging.py

    ```

- ### 3-6. generate TF-IDF analysis with the usage of integration of google news:

    ```

    After doing 3-5., calculateForNewsPulisher.py

    After doing 3-5., jiebaForNewsTitle.py  -->  copewithNewsUrl.py

    ```


- ### 3-7-1. create database(confidential):

    ```
    createForTablesAndDB.py

    ````

- ### 3-7-2. insert data into database(confidential):

    ```
    writeReferenceData() in insertLatestDataIntoDB.py  --> insertHistoricalDataIntoDB.py   --> insertLatestDataIntoDB.py

    *In the main() of insertLatestDataIntoDb.py, there are several comments for guiding how shall we do in order

    in order to successfully write data into DB.


    ```



- ### Reviewing the outcome after doing steps on the above.

> It's anticipated that we would have several json files with timestamp in folder dataMunging/cleanData, and these json files are pretty match to the data we need to render on the website.




## 4. Something to be continued...

> The content here will be updated in the following months, and thus I'm absolutely willing to improve the quality of that. Last but not least, you are able to write to me via "uncarter25le@gmail.com" if people want to know our project furthor.
