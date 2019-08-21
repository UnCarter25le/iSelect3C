# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。

import os
import sys
from bs4 import BeautifulSoup
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

def stopwordsLoad(filepath):
    with open(filepath)as f:
        inn = f.readlines()
    stopwords = [line.strip() for line in inn]
    # stopwords = [line.strip() for line in open(filepath, encoding='utf-8').readlines()]
    # print(stopwords)
    return stopwords

def wantedwordsLoad(filepath):
    with open(filepath)as f:
        inn = f.readlines()
    wantedwords = [line.strip() for line in inn]
    return wantedwords



# udn聯合新聞網': 76 https://udn.com/news/  ,
# 自由時報電子報': 63 https://news.ltn.com.tw/news   https://ec.ltn.com.tw/, 
# Yahoo奇摩新聞(新聞發布)': 59 https://tw.news.yahoo.com/, 
# '中時電子報(新聞發布)': 54 https://www.chinatimes.com/newspapers   https://www.chinatimes.com/realtimenews, 
# 'ETtoday': 44 https://www.ettoday.net/news/, 
# '經濟日報(新聞發布)': 20 https://money.udn.com/money/, 
# 'NOWnews': 13 https://www.nownews.com/news/, 
# 'TVBS新聞': 13 https://news.tvbs.com.tw/
# "東森新聞" ETtoday
_newsUrlCheckList = ["https://udn.com/news/",
                    "https://money.udn.com/money/",

                    "https://news.ltn.com.tw/news/",
                    "https://ec.ltn.com.tw/article/",
                    "https://market.ltn.com.tw/article/",
                    "https://ent.ltn.com.tw/news/",
                    # 自由時報系列；weeklybiz/paper/ 關聯性較不大。
                    # "https://news.ltn.com.tw/news/life/breakingnews/",
                    # "https://news.ltn.com.tw/news/consumer/paper/",
                    # "https://news.ltn.com.tw/news/local/paper/",
                    # "https://news.ltn.com.tw/news/focus/paper/",
                    # "https://news.ltn.com.tw/news/politics/breakingnews/",
                    # "https://news.ltn.com.tw/news/weeklybiz/paper/",
                    # "https://ec.ltn.com.tw/article/paper/",
                    # "https://ec.ltn.com.tw/article/breakingnews/",
                    # "https://ent.ltn.com.tw/news/breakingnews/",
                    # "https://ent.ltn.com.tw/news/paper/",
                    

                    "https://www.chinatimes.com/",
                    # 中國時報系列；目前兩個都ok
                    # "https://www.chinatimes.com/newspapers", 
                    # "https://www.chinatimes.com/realtimenews", 

                    "https://tw.lifestyle.appledaily.com/",
                    "https://tw.appledaily.com/",
                    # 蘋果日報系列：目前兩個都ok
                    # "https://tw.appledaily.com/headline/daily/",
                    # "https://tw.appledaily.com/new/realtime/",
                    # "https://tw.lifestyle.appledaily.com/gadget/realtime/"
                    # "https://tw.lifestyle.appledaily.com/daily/",

                    "https://tw.news.yahoo.com/", 
                    "https://www.ettoday.net/news/",
                    "https://www.nownews.com/news/", 
                    "https://news.tvbs.com.tw/life/"]

# print(_newsUrlCheckList)

# 所以一共選9家
_newsUrlCheckDict = {"udn.com":"udn聯合新聞網",
                    "money.udn.com":"經濟日報", #經濟日報(新聞發布)
                    "ltn.com":"自由時報電子報",
                    "chinatimes.com":"中時電子報", #中時電子報(新聞發布)
                    "appledaily.com":"蘋果日報", #蘋果日報(新聞發布)
                    "yahoo.com":"Yahoo奇摩新聞", #Yahoo奇摩新聞(新聞發布)
                    "ettoday.net":"ETtoday",
                    "nownews.com":"NOWnews",
                    "tvbs.com":"TVBS新聞"}