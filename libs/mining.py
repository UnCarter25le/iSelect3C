# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。

import os
import sys
import json
from bs4 import BeautifulSoup
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.manipulateDir import initialFileFirstUnderscoreString
from libs.regex import searchWordTrueOrFalse
from libs.sqlDMLAndsqlAlchemyORM import selectedNewsContentMunging
from libs.httpRequests import newsRequests


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


class newsMining(object):


    # 優化判斷
    # 1. 剔除非節能12類別的東西
    # 2. 剔除非「節能促銷」、「家電促銷」、「節能補助政策」、「家電補助政策」、「家電產業營收業績表現」相關的新聞；注意不要讓「公司股市表現、公司與公司競爭」等新聞入列
    # 3. 判定能決定新聞是否留存的關鍵字，例如：["春節", "年中慶", "週年慶", "父親節", "母親節", "618", "雙11", "88",
    #                                   ......]，如出現陣列內的字，權重必須扣1。
    # 蝦皮 99購物節、蘇寧818購物節
    # 2018年開始 雙十購物節、 (國慶)家家購物節--------若此購物時間開始像雙11那樣習以為常，那麼就得轉變成停用詞
    # 『百貨』目前沒有被列入停用或想要的字典之中，不過它可以帶出 非一般所熟知的促銷檔期，例如 雙十購物。*一般所熟知的就是週年慶、父親母親節...。
    _lastCheckForUnwantedWords = ["春節", "年中慶", "周年慶", "週年慶", "父親節", "母親節", "618", "雙11", "88", "618",
                                       "1111", "11.11", "6.18", "聰明用電", "機車", "汽機車", "老車", "計程車", "車齡",
                                      "汽車", "柴油車", "貨車", "車種", "新北富基漁港", "營收輸給", "業績輸給", "填息", "4K彩電", "816",
                                      "818","這家電商", "飲品", "電視", "雙十一", "雙12", "雙十二", "12.12", "99購物", "中國國慶", "台灣萊雅",
                                      "尾牙", "年貨"]




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


    
    def judgeFolderFiles(self, dirRoute):
        fileName = initialFileFirstUnderscoreString(dirRoute)
        if not fileName:
            return fileName, 0
        else:
            return fileName, len(fileName)


    def loadOneFileIn(self, fileCompleteRoute):
        with open(fileCompleteRoute)as f:
            jsonFile = json.load(f)
        return jsonFile

    def judgeHowToCrawl(self, newsLink, referenceFile):
        """
        針對切字切詞、出版社篩選後的新聞集，進型匹配的爬蟲。
        
        """
        publisher_Id, publisher = None, None

        for checkLink in self._newsUrlCheckDict:    
            if searchWordTrueOrFalse(checkLink, newsLink):

                publisher = self._newsUrlCheckDict.get(checkLink)
                publisher_Id = selectedNewsContentMunging().judgePublisherId(publisher, referenceFile)
                
                print("準備擷取：", publisher, newsLink)
                break
            
        videoLinkInContent, newsContent = newsRequests().intersectionForCrawl(publisher, newsLink)

        return publisher_Id, publisher, videoLinkInContent, newsContent
