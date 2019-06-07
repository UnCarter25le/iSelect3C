
# Preface
## "iSelect3C" is the project powered by Tom, JiaSyuan, and I(Carter).
- The project was created for OPEN DATA Innovative Application Contest, which was hosted by several Government Departments on 2019 May.
- The project's intention is to reduce the information gap between consumers and sellers, especially when a consumer is eaget to puchase energy-saving consumer electronics which's certification is within the validity period. 
- In addtion, we offer simple but comprehensive calculator to leave users to have better understanding of something worthwhile to watch, such as what possible eletronic fees is and how it cost under the official specifications provided by Bureau of Energy of of Ministry of Economic Affairs.
- The mvp website is " http://herbmagicwebapi.azurewebsites.net/iselect3C " , and we all know that is not enough to see it as an mature web application. But still, it has enabled users to pick out the products that are validated by government from e-commerce, pchome and momo.

--------
--------
--------

# These section are the zone of development. 

## 1. Environment:
- python 3.6.8


## 2. The structure of my contribution(data acquisition and munging):

```
/cralwer
    |___pchomeApi.py______________________> Crawling date in one main process way via api.
    |___pchomeApiMulti.py_________________> Crawling date in a multiprocess manner via api.
    |___momoMulti.py______________________> Crawling date in a multiprocess(selenium) manner. 
                                            Noting that it must kill chrome process 
                                            mannally after executing this program.
    |___bureauEnergyMulti_1.py____________> Crawling date in a multiprocess manner.
    |___bureauEnergyMulti_2.py____________> Crawling date in a multiprocess manner.
    
/dataMunging
    |___pchomeMunging.py____________> Munging date, json format, after having raw data in 
                                      "/rawData/pchome/冷暖空調/「24h」「kdn」「vdr」".
    |___momoMunging.py______________> Munging date, text format, after having raw data in 
                                      "/rawData/momo/「冷暖空調」「電冰箱」「除濕機」.., and you name it".
    |___bureauEnergyMunging.py______> Munging date, text format, after having raw data in
                                      "/rawData/bureauEnergy/「冷暖空調」「電冰箱」「除濕機」.., and you name   
                                      it".
    
    |___cleanData___________________> storing the data, json format, which is ready for inserting into DB.
            |___bureauEnergy/
            |___momo/
            |___pchome/

    |___rawData
            |___bureauEnergy/
                    |___無風館空氣調節機
                            |___overview/
                            |___deatil/
                            |___XXX.json
                            |___OOO.json
                    |___ many other you name it.
            |___momo/
                |___冷暖空調/
                |___ many other you name it.
            |___pchome/
                |___冷暖空調/
                        |___ 24h/
                        |___ kdn/
                        |___ vdr/

/libs
    |___ manipulateDir.py____________> mkdir or rmdir whenever we wanna make crawling or munging.
    |___ multiProcessing.py__________> Needed by programs those operations are in a mulitprocess manner.
    |___ munging.py__________________> Needed by programs which are ready to process raw data.
    |___ regex.py____________________> Used in the situations in which we wanna extract accurate data type
                                       from raw data.
    |___ splinterBrowser.py__________> Used by programs which require chromdirver to start browser.
    |___ time.py_____________________> Used when the interval peiod is needed in programs' processing.



/doc
    |___iSelect3C使用案例圖.png________> Overview for use case diagram.
    |___iSelect3C活動圖.png___________> Overview for activity diagram.

/___
    |___README.md
    |___requirements.txt_____________> Packages my environment installed.


```


## 3. The process of executing the ".py" file:

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

- ### 3-4. Reviewing the outcome after doing steps 3-1, 3-2, 3-2.

> It's anticipated that we would have several json files with timestamp in folder dataMunging/cleanData, and these json files are pretty match to the data we need to render on the website.




## 4. Something to be continued...

> The content here will be updated in the following months, and thus I'm absolutely willing to improve the quality of that. Last but not least, you are able to write to me via "uncarter25le@gmail.com" if people want to know our project furthor.
