
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
    |___weatherObservationStation.py.py___> Crawling data in one main process way(selenium) from official web site.
    |___weatherRecordMulti.py.py__________> Crawling date in a multiprocess manner from official web site.
    
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
    |       |___pchome/
    |       |___observationStation/
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
            |       |___ many other you name it.
            |
            |___momo/
            |   |___冷暖空調/
            |   |   |___1_67_冷暖空調.txt
            |   |   |___many other you name it.
            |   |___ many other you name it.
            |
            |___pchome/
            |   |___冷暖空調/
            |           |___ 24h/
            |           |   |___1_62_1233_24h冷暖空調.json
            |           |   |___many other you name it.
            |           |___ kdn/
            |           |___ vdr/
            |
            |___weather/
            |   |___2009/
            |   |   |___2009_1.txt
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



/libs/
    |___ manipulateDir.py_________________> mkdir or rmdir whenever we wanna make crawling or munging.
    |___ multiProcessing.py_______________> Needed by programs those operations are in a mulitprocess manner.
    |___ munging.py_______________________> Needed by programs which are ready to process raw data.
    |___ regex.py_________________________> Used in the situations in which we wanna extract accurate data type
    |                                       from raw data.
    |___ splinterBrowser.py_______________> Used by programs which require chromdirver to start up browsers.
    |___ time.py__________________________> Used when the interval peiod is needed in programs' processing.
    |___ requests.py______________________> Be imported while the useage of the fixed parameters.



/doc/
    |___iSelect3C使用案例圖.png_____________> Overview for use case diagram.
    |___iSelect3C活動圖.png________________> Overview for activity diagram.
    |___chromedriver______________________> according to: http://chromedriver.chromium.org/downloads
                                            editionInfo: ChromeDriver 75.0.3770.90
                                            execute `sudo cp chromedriver /usr/local/bin/`

/___
    |___README.md
    |___.gitignore
    |___requirements.txt__________________> Packages my environment installed.


```


## 3. The process of executing the ".py" file:

- ### 3-1. pchome, the order of executing:

    ```
    pchomeApi.py  or  pchomeApiMulti.py  -->  pchomeMunging.py

    ```

- ### 3-2. momo, the order of executing:

    ```
    Note: Since chrome browsers driven by chromedriver would be definitely watched by momo's IT protection, 
    the numbers of getPageInARowAdvanced_proc(process ready to be created) has better to be match to the real numbers of pages on momo website.

    We are abel to modify the object "_momoKeywordUrlPair" in multiProcessing.py to complete crawling jobs.

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



- ### Reviewing the outcome after doing steps on the above.

> It's anticipated that we would have several json files with timestamp in folder dataMunging/cleanData, and these json files are pretty match to the data we need to render on the website.




## 4. Something to be continued...

> The content here will be updated in the following months, and thus I'm absolutely willing to improve the quality of that. Last but not least, you are able to write to me via "uncarter25le@gmail.com" if people want to know our project furthor.
