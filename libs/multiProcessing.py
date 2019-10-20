# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os
import sys
from bs4 import BeautifulSoup
_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.timeWidget import timeSleepOne
from libs.timeWidget import timeStampGenerator
from libs.manipulateDir import initialFileZeroUnderscoreInt
from libs.regex import interDiv
from libs.regex import searchFloatNums
# from libs.regex import searchNums
from libs.regex import floatDiv


def distributeKeyword(keywordUrlPair, output):
    for keyword in keywordUrlPair:
        print('distributeKeyword in main process %s' %os.getpid())
        output.put(keyword)
        print("這裡是distributeKeyword，準備送給  接下來的進程  處理: " + keyword)
        timeSleepOne() #暫停幾秒來模擬現實狀況。

def selectColumn(textSoup, row):
    selected = textSoup.find('div',{'class':'row text-center col-sm-12'}).select('.row')[row].text
    selected = selected.split('：')[1]
    return selected

_monthsAvailable = [str(row) for row in range(1,13)]

_weatherRecordAvailable = {"2009": _monthsAvailable,
                        "2010": _monthsAvailable,
                        "2011": _monthsAvailable,
                        "2012": _monthsAvailable,
                        "2013": _monthsAvailable,
                        "2014": _monthsAvailable,
                        "2015": _monthsAvailable,
                        "2016": _monthsAvailable,
                        "2017": _monthsAvailable,
                        "2018": _monthsAvailable,
                        "2019": [str(row) for row in range(1,10)]}


# 除濕機與電冰箱是採「107年新分級基準」。
# 瓦斯熱水器(即熱式燃氣熱水器)
# 瓦斯爐(燃氣台爐)
_bureauEnergyKeywordUrlPair = {"無風管空氣調節機":("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=49"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "除濕機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=55"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "電冰箱" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=56"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "電熱水瓶" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=47"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "溫熱型開飲機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=50"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "溫熱型飲水機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=53"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "冰溫熱型開飲機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=52"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "冰溫熱型飲水機" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=54"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "貯備型電熱水器": ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=48"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "瓦斯熱水器": ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=46"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "瓦斯爐" : ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=45"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "安定器內藏式螢光燈泡": ("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=38"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno=")
                                }

_googleSearchWord = {"家電促銷":"https://www.google.com/",
                     "家電汰舊換新":"https://www.google.com/",
                     "家電節能補助":"https://www.google.com/"}


# https://www.momoshop.com.tw/search/searchShop.jsp?
# keyword=%E7%93%A6%E6%96%AF%E7%86%B1%E6%B0%B4%E5%99%A8
# &searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType
_momoKeywordUrlPair = {"冷暖空調":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF"
                        "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "除濕機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E9%99%A4%E6%BF%95%E6%A9%9F"
                        "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "電冰箱":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E9%9B%BB%E5%86%B0%E7%AE%B1"
                        "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "電熱水瓶":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E9%9B%BB%E7%86%B1%E6%B0%B4%E7%93%B6"
                        "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
                        "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp?"
                        "keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
                        "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "冰溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
                                "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "冰溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
                                "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "貯備型電熱水器":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E8%B2%AF%E5%82%99%E5%9E%8B%E9%9B%BB%E7%86%B1%E6%B0%B4%E5%99%A8"
                                "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "瓦斯熱水器":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E7%93%A6%E6%96%AF%E7%86%B1%E6%B0%B4%E5%99%A8"
                                "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "瓦斯爐":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E7%93%A6%E6%96%AF%E7%88%90"
                                "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType"),
                # 安定器內藏式螢光燈泡 momo找不到品項，導致找到很多很多高價位汽車。
                "節能燈泡":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E5%AE%89%E5%AE%9A%E5%99%A8%E5%85%A7%E8%97%8F%E5%BC%8F%E8%9E%A2%E5%85%89%E7%87%88%E6%B3%A1"
                                "&searchType=3&curPage=1&_isFuzzy=1&showType=chessboardType")}

_pchomeKeywordUrlPair = {"冷暖空調":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "除濕機":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "電冰箱":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "電熱水瓶":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "溫熱型開飲機":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "溫熱型飲水機":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "冰溫熱型開飲機":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "冰溫熱型飲水機":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "貯備型電熱水器":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "瓦斯熱水器":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "瓦斯爐":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "節能燈泡":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc"}