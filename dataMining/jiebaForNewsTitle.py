# -*- coding:utf-8 -*-

"""
程式名稱：
程式描述：


備　　註：

    此檔案一開始命名為jieba.py，致使python import module時，一直引用到「dataMining/jieba.py」



    春節、年中慶、週年慶、父親節、母親節、618、雙11  優惠的商品種類太多，不限家電，因此排除
    雙11
1111
11.11
618
6.18
苏宁818

    呼籲  聰明用電   是節電的新聞


    ＊要抓的是家電促銷、家電補助申請等新聞

"""
import os
import sys
import json
import jieba
import math
from collections import Counter
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)

from libs.mining import stopwordsLoad
from libs.mining import wantedwordsLoad
from libs.regex import searchWordTrueOrFalse


def loadOneFileIn():
    fileName = os.listdir(dirRoute)
    fileName.sort(key= lambda x: x.split('_')[1])
    fileName = fileName.pop()
    print(fileName)
    with open(dirRoute + "/" + fileName)as f:
        inn = json.load(f)
    newsObject = inn["newsUrl"]
    print("新聞標題總數量：", len(newsObject))

    return newsObject

def loadManyFilesIn():
    fileName = os.listdir(dirRoute)
    print(fileName)
    newsObject = {}
    for file in fileName:
        with open(dirRoute + "/" + file)as f:
            inn = json.load(f)
        newsObject.update(inn["newsUrl"])
        print(len(newsObject))

    return newsObject



if __name__ == '__main__':

    objectiveFolder = "rawData"

    objectiveFolderDataMining = "dataMining"
    
    objectiveFolderDictionary = "dictionary"

    objective = "news"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/newsIntegration"

    counterNum = Counter()
    TFIDF = Counter()



    # 載入字典：
    # 強化字
    wantedwords = wantedwordsLoad(f"{_BASE_PATH}/{objectiveFolderDataMining}/{objectiveFolderDictionary}/newsTitle_wanted_words.txt")
    for word in wantedwords:
        jieba.add_word(word)
    # 這裡讀取的stop_word只針對jieba.analyze()方法時有用！
    # jieba.analyse.set_stop_words("/home/bluevc/VIRTUALENV/iSelect3CPY36/lib/python3.6/site-packages/jieba/stop_words.txt")
    # 要對jieba.cut()有作用的停用詞，則需要自己製作得出！   #(' ', 72) 把空白放在stop_words.txt裡面，沒法發揮效果，因此要在程式裡解決。
    stopwords = stopwordsLoad(f"{_BASE_PATH}/{objectiveFolderDataMining}/{objectiveFolderDictionary}/newsTitle_stop_words.txt")


    newsObject = loadOneFileIn()
    newsString = ""
    for key in newsObject:
        newsString += newsObject[key][0] + "＋"
    
    jiebaGenerator = jieba.cut(newsString)
    jiebaListExceptStopwords = [word for word in jiebaGenerator if not word in stopwords and word != ' ']

    for word in jiebaListExceptStopwords:
        if word in counterNum:
            counterNum[word] += 1
        else:
            counterNum[word] = 1

    print("統計頻率字結果：")
    print(counterNum.most_common(100))
    # print(counterNum["Digital"])
    # print(counterNum["Panasonic"])
    # print(counterNum["City"])
    # print(counterNum["PChome"])
    # print(counterNum["PChome24h"])

    
    newsList = [newsObject[key][0] for key in newsObject] #新聞標題陣列
    newsListNums = len(newsObject)  #總文章數

    for k, v in counterNum.items():
        specificwordTF = v
        specificwordFrequency = 0


        #計算個別字的IDF
        for news in newsList:
            specificwordFrequency += searchWordTrueOrFalse(k, news)
        try:
            specificwordIDF = math.log((newsListNums / specificwordFrequency), 10)
            TFIDF[k] = specificwordTF * specificwordIDF
        except ZeroDivisionError as e:
            print("這個切詞有問題：", k)
            raise
    
    print("個別字TFIDF結果：")
    
    # print(TFIDF.most_common(3505)[3300:][::-1])
    print()
    print(TFIDF.most_common(100))


    # with open(f"{_BASE_PATH}/{objectiveFolderDataMining}/{objectiveFolderDictionary}/jiebaCut_resultOfNewsTitle.json", "w", encoding="utf-8") as f:
    #     json.dump(counterNum.most_common(100),f, indent=2, ensure_ascii=False)

    # with open(f"{_BASE_PATH}/{objectiveFolderDataMining}/{objectiveFolderDictionary}/TFIDF_resultOfNewsTitle.json", "w", encoding="utf-8") as f:
    #     json.dump(TFIDF.most_common(100),f, indent=2, ensure_ascii=False)

    
    

    

# udn聯合新聞網': 76 https://udn.com/news/  ,
# 自由時報電子報': 63 https://news.ltn.com.tw/news   https://ec.ltn.com.tw/, 
# Yahoo奇摩新聞(新聞發布)': 59 https://tw.news.yahoo.com/, 
# '中時電子報(新聞發布)': 54 https://www.chinatimes.com/newspapers   https://www.chinatimes.com/realtimenews, 
# 'ETtoday': 44 https://www.ettoday.net/news/, 
# '經濟日報(新聞發布)': 20 https://money.udn.com/money/, 
# 'NOWnews': 13 https://www.nownews.com/news/, 
# 'TVBS新聞': 13 https://news.tvbs.com.tw/




