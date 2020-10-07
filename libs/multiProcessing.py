# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os
import sys
from bs4 import BeautifulSoup
import random
_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.timeWidget import (timeSleepOne,
                        timeStampGenerator,
                        timeSleepRandomly)
from libs.manipulateDir import initialFileZeroUnderscoreInt
from libs.regex import interDiv
from libs.regex import searchFloatNums
# from libs.regex import searchNums
from libs.regex import floatDiv

from libs.splinterBrowser import (
                                browserWaitTime
                                )


class keywordResourcePair(object):

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
                                "2019": _monthsAvailable, 
                                "2020": ["1", "2"]}


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

        #momo摩天商城得用spinter
        # https://www.momomall.com.tw/mmlsearch/%E9%99%A4%E6%BF%95%E6%A9%9F.html
        # https://www.momomall.com.tw/mmlsearch/%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF.html
        _momoMallKeywordUrlPair = {"冷暖空調":("https://www.momomall.com.tw/mmlsearch/"
                                "%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF.html"),
                        "除濕機":("https://www.momomall.com.tw/mmlsearch/"
                                "%E9%99%A4%E6%BF%95%E6%A9%9F.html"),
                        "電冰箱":("https://www.momomall.com.tw/mmlsearch/"
                                "%E9%9B%BB%E5%86%B0%E7%AE%B1.html"),
                        "電熱水瓶":("https://www.momomall.com.tw/mmlsearch/"
                                "%E9%9B%BB%E7%86%B1%E6%B0%B4%E7%93%B6.html"),
                        "溫熱型開飲機":("https://www.momomall.com.tw/mmlsearch/"
                                "%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F.html"),
                        "溫熱型飲水機":("https://www.momomall.com.tw/mmlsearch/"
                                "%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F.html"),
                        "冰溫熱型開飲機":("https://www.momomall.com.tw/mmlsearch/"
                                        "%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F.html"),
                        "冰溫熱型飲水機":("https://www.momomall.com.tw/mmlsearch/"
                                        "%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F.html"),
                        "貯備型電熱水器":("https://www.momomall.com.tw/mmlsearch/"
                                        "%E8%B2%AF%E5%82%99%E5%9E%8B%E9%9B%BB%E7%86%B1%E6%B0%B4%E5%99%A8.html"),
                        "瓦斯熱水器":("https://www.momomall.com.tw/mmlsearch/"
                                        "%E7%93%A6%E6%96%AF%E7%86%B1%E6%B0%B4%E5%99%A8.html"),
                        "瓦斯爐":("https://www.momomall.com.tw/mmlsearch/"
                                        "%E7%93%A6%E6%96%AF%E7%88%90.html"),
                        # 安定器內藏式螢光燈泡 momo找不到品項，導致找到很多很多高價位汽車。
                        "節能燈泡":("https://www.momomall.com.tw/mmlsearch/"
                                        "%E7%AF%80%E8%83%BD%E7%87%88%E6%B3%A1.html")}

        # https://www.momoshop.com.tw/search/searchShop.jsp?
        # keyword=%E7%93%A6%E6%96%AF%E7%86%B1%E6%B0%B4%E5%99%A8
        # &searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType
        _momoKeywordUrlPair = {"冷暖空調":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "除濕機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E9%99%A4%E6%BF%95%E6%A9%9F"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "電冰箱":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E9%9B%BB%E5%86%B0%E7%AE%B1"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "電熱水瓶":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E9%9B%BB%E7%86%B1%E6%B0%B4%E7%93%B6"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp?"
                                "keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "冰溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                        "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
                                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "冰溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                        "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
                                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "貯備型電熱水器":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                        "?keyword=%E8%B2%AF%E5%82%99%E5%9E%8B%E9%9B%BB%E7%86%B1%E6%B0%B4%E5%99%A8"
                                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "瓦斯熱水器":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                        "?keyword=%E7%93%A6%E6%96%AF%E7%86%B1%E6%B0%B4%E5%99%A8"
                                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "瓦斯爐":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                        "?keyword=%E7%93%A6%E6%96%AF%E7%88%90"
                                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        # 安定器內藏式螢光燈泡 momo找不到品項，導致找到很多很多高價位汽車。
                        "節能燈泡":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                        "?keyword=%E7%AF%80%E8%83%BD%E7%87%88%E6%B3%A1"
                                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                        "電鍋":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                        "?keyword=%E9%9B%BB%E9%8D%8B"
                                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType")}

                                        

        # https://ecshweb.pchome.com.tw/search/v3.3/24h/results?q=冷暖空調&page=1&sort=sale/dc
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
                                "節能燈泡":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                                "電鍋":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc"}




class multiProcessToolBox(keywordResourcePair):

        @classmethod
        def distributeKeyword(cls, keywordUrlPair, output):
                for keyword in keywordUrlPair:
                        print('distributeKeyword in main process %s' %os.getpid())
                        output.put(keyword)
                        print("這裡是distributeKeyword，準備送給  接下來的進程  處理: " + keyword)
                        timeSleepOne() #暫停幾秒來模擬現實狀況。
        @classmethod
        def selectColumn(cls, textSoup, row):
                selected = textSoup.find('div',{'class':'row text-center col-sm-12'}).select('.row')[row].text
                selected = selected.split('：')[1]
                return selected

        

        
        # browser.find_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/dl/dd[1]/a').click()
        class momoMallBrowser(object):
                @classmethod
                def browserClickNextPage(cls, browser):
                        """
                        momoMall用到！
                        """
                        browser.find_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/dl/dd[1]/a').click()
                        
                @classmethod
                def browserCheckNextPage(cls, browser):
                        """
                        momoMall用到！
                        """
                        nextPage = browser.find_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/dl/dd[1]/a')

                        return nextPage.text
                

                @classmethod
                def browserClickPageNumber(cls, browser, currentPage, totalPage, searchword):
                        """
                        #點擊頁數
                        # 預設
                        # 1 2 3 4 5 6 7 8 9 10 >> >|
                        # 頂 上10頁
                        # 1                                      14
                        # |< << 11 12 13 14 15 16 17 18 19 20 >> >|

                        # accuratePage =  browser.find_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/ul/li[8]/a')
                        accuratePage =  browser.find_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/ul/li[1]/a')
                        accuratePage.text
                        """
                        
                        currentPageNum = int(currentPage)
                        if currentPageNum <= 10:
                                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{currentPageNum}]/a').click()
                                accuratePage = browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{currentPageNum}]/a').text
                                
                        elif 11 <= currentPageNum <= 20:
                                #去到11~20頁
                                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[11]/a').click()
                                clickNum =  currentPageNum - 10 + 2
                                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{clickNum}]/a').click()
                                accuratePage = browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{clickNum}]/a').text
                        else:
                                #去到11~20頁
                                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[11]/a').click()
                                
                                clickNextTimes = currentPageNum // 10
                                #點擊到正確頁數的畫面
                                for i in range(clickNextTimes-1):
                                        browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[13]/a').click()
                                        timeSleepRandomly()
                                        timeSleepOne()
                                
                                #點擊到正確頁碼
                                judgeNum =  currentPageNum - (clickNextTimes * 10)
                                if judgeNum:
                                        clickNum =  judgeNum + 2
                                elif judgeNum == 0:
                                        clickNum =  judgeNum + 12
                                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{clickNum}]/a').click()
                                accuratePage = browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{clickNum}]/a').text
                        
                        print(f"{searchword}__目標頁碼:{currentPage}, 點擊頁碼:{accuratePage}, 總頁數:{totalPage}")

                @classmethod
                def browserClickSearchType(cls, browser, positionNum):
                        """
                        momoMall用到！

                        searchType:1 準確度  leader
                        searchType:2 價格由小至大  prdPrice initial choice
                        searchType:3 價格由大至小  
                        searchType:4 新上市   newPrd
                        searchType:5 熱銷排行  hot

                        每次點擊，頁數都回至1
                        

                        //*[@id="bt_2_layout_Content"]/div[3]/span/ul/li[1] leader
                        //*[@id="bt_2_layout_Content"]/div[3]/span/ul/li[2] newPrd
                        //*[@id="bt_2_layout_Content"]/div[3]/span/ul/li[3] hot
                        //*[@id="bt_2_layout_Content"]/div[3]/span/ul/li[4] prdPrice
                        

                        倘若網址導向https://www.momomall.com.tw/main/Main.jsp，
                        就沒有searchType可以點擊，發生
                        AttributeError: 'ElementList' object has no attribute 'text'
                        """

                        buyingTendency = browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[3]/span/ul/li[{positionNum}]').text
                        browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[3]/span/ul/li[{positionNum}]').click()

                        # selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: element is not attached to the page document
                        # return buyingTendency.text
                        
                        return buyingTendency
                
                



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
                        "2019": _monthsAvailable, 
                        "2020": ["1", "2"]}


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
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                     "電鍋":("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=57"
                                "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno=")
                                }

_googleSearchWord = {"家電促銷":"https://www.google.com/",
                     "家電汰舊換新":"https://www.google.com/",
                     "家電節能補助":"https://www.google.com/"}

#momo摩天商城得用spinter
_momomallKeywordUrlPair = {"冷暖空調":("https://www.momomall.com.tw/mmlsearch/"
                        "%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF.html"),
                "除濕機":("https://www.momomall.com.tw/mmlsearch/"
                        "%E9%99%A4%E6%BF%95%E6%A9%9F.html"),
                "電冰箱":("https://www.momomall.com.tw/mmlsearch/"
                        "%E9%9B%BB%E5%86%B0%E7%AE%B1.html"),
                "電熱水瓶":("https://www.momomall.com.tw/mmlsearch/"
                        "%E9%9B%BB%E7%86%B1%E6%B0%B4%E7%93%B6.html"),
                "溫熱型開飲機":("https://www.momomall.com.tw/mmlsearch/"
                        "%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F.html"),
                "溫熱型飲水機":("https://www.momomall.com.tw/mmlsearch/?"
                        "%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F.html"),
                "冰溫熱型開飲機":("https://www.momomall.com.tw/mmlsearch/"
                                "%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F.html"),
                "冰溫熱型飲水機":("https://www.momomall.com.tw/mmlsearch/"
                                "%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F.html"),
                "貯備型電熱水器":("https://www.momomall.com.tw/mmlsearch/"
                                "%E8%B2%AF%E5%82%99%E5%9E%8B%E9%9B%BB%E7%86%B1%E6%B0%B4%E5%99%A8.html"),
                "瓦斯熱水器":("https://www.momomall.com.tw/mmlsearch/"
                                "%E7%93%A6%E6%96%AF%E7%86%B1%E6%B0%B4%E5%99%A8.html"),
                "瓦斯爐":("https://www.momomall.com.tw/mmlsearch/"
                                "%E7%93%A6%E6%96%AF%E7%88%90.html"),
                # 安定器內藏式螢光燈泡 momo找不到品項，導致找到很多很多高價位汽車。
                "節能燈泡":("https://www.momomall.com.tw/mmlsearch/"
                                "%E7%AF%80%E8%83%BD%E7%87%88%E6%B3%A1.html")}

# https://www.momoshop.com.tw/search/searchShop.jsp?
# keyword=%E7%93%A6%E6%96%AF%E7%86%B1%E6%B0%B4%E5%99%A8
# &searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType
_momoKeywordUrlPair = {"冷暖空調":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E5%86%B7%E6%9A%96%E7%A9%BA%E8%AA%BF"
                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "除濕機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E9%99%A4%E6%BF%95%E6%A9%9F"
                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "電冰箱":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E9%9B%BB%E5%86%B0%E7%AE%B1"
                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "電熱水瓶":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E9%9B%BB%E7%86%B1%E6%B0%B4%E7%93%B6"
                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                        "?keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp?"
                        "keyword=%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "冰溫熱型開飲機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%96%8B%E9%A3%B2%E6%A9%9F"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "冰溫熱型飲水機":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E5%86%B0%E6%BA%AB%E7%86%B1%E5%9E%8B%E9%A3%B2%E6%B0%B4%E6%A9%9F"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "貯備型電熱水器":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E8%B2%AF%E5%82%99%E5%9E%8B%E9%9B%BB%E7%86%B1%E6%B0%B4%E5%99%A8"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "瓦斯熱水器":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E7%93%A6%E6%96%AF%E7%86%B1%E6%B0%B4%E5%99%A8"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "瓦斯爐":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E7%93%A6%E6%96%AF%E7%88%90"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                # 安定器內藏式螢光燈泡 momo找不到品項，導致找到很多很多高價位汽車。
                "節能燈泡":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                "?keyword=%E7%AF%80%E8%83%BD%E7%87%88%E6%B3%A1"
                                "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType"),
                "電鍋":("https://www.momoshop.com.tw/search/searchShop.jsp"
                                        "?keyword=%E9%9B%BB%E9%8D%8B"
                                        "&searchType=1&curPage=1&_isFuzzy=1&showType=chessboardType")}

# https://ecshweb.pchome.com.tw/search/v3.3/24h/results?q=冷暖空調&page=1&sort=sale/dc
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
                         "節能燈泡":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc",
                         "電鍋":"https://ecshweb.pchome.com.tw/search/v3.3/{0}/results?q={1}&page={2}&sort=sale/dc"}