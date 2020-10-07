# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。

from bs4 import BeautifulSoup
import requests
import random
import os
import sys

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

from libs.timeWidget import (
                            timeSleepRandomly,
                            timeSleepOne,
                            timeSleepTwo,
                            timeSleepThree,
                            timeSleepFour
                            )
from libs.regex import (
                        textMiningRegex,
                        urlParseDealing,
                        searchWordTrueOrFalse
                        )

from libs.splinterBrowser import (
                              buildSplinterBrowser,
                              buildSplinterBrowserHeadless,
                              browserWaitTime
                                )

_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}


# def proxiesIpGenerator():
#     """
#     check the ip address we carry : http://ip.filefab.com/index.php
#     proxy ips for reference : https://cn-proxy.com/
#     """
#     proxy_ips = ['124.156.108.71:82', '60.217.143.23:8060', '116.114.19.204:443']
#     proxy_ip = random.Choice(proxy_ips)
#     res = requests.get(url, headers=headers, proxies = {"http": "http://"+proxy_ip })

#     print('Use', ip)
#     resp = requests.get('http://ip.filefab.com/index.php',
#                         proxies={'http': 'http://' + ip})
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     print(soup.find('h1', id='ipd').text.strip())
    


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
                                    "&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&pageno="),
                    "電鍋":("https://ranking.energylabel.org.tw/product/Approval/list.aspx"
                                    "?&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=57"
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
                                    "%E7%AF%80%E8%83%BD%E7%87%88%E6%B3%A1.html"),
                    "電鍋":("https://www.momomall.com.tw/mmlsearch/"
                                    "%E9%9B%BB%E9%8D%8B.html")}

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
                    # https://www.momoshop.com.tw/search/searchShop.jsp?keyword=%E9%9B%BB%E9%8D%8B
                    # &searchType=1&cateLevel=0&cateCode=&curPage=1&_isFuzzy=0&showType=chessboardType

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




class ecommerceProductsRequests(object):
    
    _headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}


    _eCommercePchome24 = "pchome24" #https://24h.pchome.com.tw/

    _eCommerceMomo = "momo" #https://www.momoshop.com.tw/main/Main.jsp  # 有規格篩選

    _eCommerceMomoMall = "momoMall" #https://www.momomall.com.tw/main/Main.jsp  #有商品分類

    _eCommerceCarrefour = "carrefour" #https://online.carrefour.com.tw/

    _eCommerceRtmart = "rtmart" #https://www.rt-mart.com.tw/direct/

    _eCommerceRakuten = "rakuten" #https://www.rakuten.com.tw/

    _eCommerceShapee = "shapee" # 新商品 https://shopee.tw/

    _eCommerceYahooMall = "yahoomall" #https://tw.mall.yahoo.com/

    _eCommerceEtMall = "etmall" #https://www.etmall.com.tw/


    def __init__(self, *args, **kwargs):
        self.keywordResourcePair = kwargs.get("keywordResourcePair", "")
        
    # @classmethod
    def intersectionForCrawl(self, ecommerceName, ecommerceLink=None):


        if ecommerceName == self._eCommerceMomoMall:
            browser = buildSplinterBrowserHeadless('chrome')

            return browser
        else:
            return None


class pchome24Requests(ecommerceProductsRequests):
    
    pass

class momoRequests(ecommerceProductsRequests):
    
    pass

class momoMallRequests(ecommerceProductsRequests):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
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
        
        # 置底
        # |< << 281 282 283 284

        # accuratePage =  browser.find_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/ul/li[8]/a')
        accuratePage =  browser.find_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/ul/li[1]/a')
        accuratePage.text
        """
        
        currentPageNum = int(currentPage)
        totalPageNum = int(totalPage)
        halfTotalPageNum = totalPageNum // 2


        if currentPageNum > halfTotalPageNum and currentPageNum > 10:
            #去到置底頁
            browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[12]/a').click()
            timeSleepOne()
            
            
            if currentPageNum != totalPageNum and currentPageNum // 10 == totalPageNum // 10:
                if currentPageNum % 10 != 0:
                    # 13、18
                    clickBeforeTimes = 0
                elif  currentPageNum % 10 == 0:
                    # 290、299
                    clickBeforeTimes = 1
                
                #反方向點擊到正確頁數的畫面
                for i in range(clickBeforeTimes):
                    browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[2]/a').click()
                    # timeSleepRandomly()
                    # timeSleepOne()
                    browserWaitTime(browser)

            elif currentPageNum != totalPageNum and currentPageNum // 10 < totalPageNum // 10:

                if  currentPageNum % 10 != 0 and totalPageNum % 10 == 0:# and totalPageNum - currentPageNum < 10:
                    # 281、290    
                    # 271、290
                    # 11、30
                    clickBeforeTimes = (totalPageNum // 10) - (currentPageNum // 10) - 1

                elif  currentPageNum % 10 != 0 and totalPageNum % 10 != 0:# and totalPageNum - currentPageNum >= 10:
                    # 271、291
                    # 18、23
                    clickBeforeTimes = (totalPageNum // 10) - (currentPageNum // 10)
                
                elif  currentPageNum % 10 == 0 and totalPageNum % 10 != 0:
                    # 270、291
                    clickBeforeTimes = (totalPageNum // 10) - (currentPageNum // 10) + 1

                elif  currentPageNum % 10 == 0 and totalPageNum % 10 == 0:
                    # 270、290
                    clickBeforeTimes = (totalPageNum // 10) - (currentPageNum // 10)
                
                #反方向點擊到正確頁數的畫面
                for i in range(clickBeforeTimes):
                    browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[2]/a').click()
                    # timeSleepRandomly()
                    # timeSleepOne()
                    browserWaitTime(browser)
            
            #點擊到正確頁碼
            judgeNum = currentPageNum % 10
            if judgeNum:
                clickNum =  judgeNum + 2
            elif judgeNum == 0:
                clickNum =  judgeNum + 12
            print(f"反方向__{searchword}__目標頁碼:{currentPage}, 點擊項次:{clickNum}, 總頁數:{totalPage}")
            browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{clickNum}]/a').click()
            accuratePage = browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{clickNum}]/a').text
        
            print(f"反方向__{searchword}__目標頁碼:{currentPage}, 點擊頁碼:{accuratePage}, 總頁數:{totalPage}")
            
        else:
            if currentPageNum <= 10:
                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{currentPageNum}]/a').click()
                accuratePage = browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{currentPageNum}]/a').text
                    
            elif 11 <= currentPageNum <= 20:
                #去到11~20頁
                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[11]/a').click()
                clickNum =  currentPageNum - 10 + 2
                timeSleepOne()
                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{clickNum}]/a').click()
                accuratePage = browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{clickNum}]/a').text
            else:
                #去到11~20頁
                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[11]/a').click()
                
                
                if currentPageNum % 10 == 0:
                    # 電冰箱__目標頁碼:290, 點擊頁碼:300, 總頁數:921
                    clickNextTimes = currentPageNum // 10 - 1
                else:
                    # 冰箱__目標頁碼:292, 點擊頁碼:292, 總頁數:921
                    clickNextTimes = currentPageNum // 10
                
                #點擊到正確頁數的畫面
                for i in range(clickNextTimes-1): #扣1是因為已經「#去到11~20頁」
                    browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[13]/a').click()
                    # timeSleepRandomly()
                    # timeSleepOne()
                    browserWaitTime(browser)
                
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
    
    @classmethod
    def humanSimulate(cls, browser):
        """
        之所以click()不成功是因為mouse_over後，browser視窗看不到要點擊的xpath了！
        
        WebDriverException: Message: unknown error: Element <a class="selected">...</a> is not clickable at point (338, 13). Other element would receive the click: <div id="bt_0_002_01" class="">...</div>
        (Session info: chrome=80.0.3987.122)
        (Driver info: chromedriver=2.36.540471 (9c759b81a907e70363c6312294d30b6ccccc2752),platform=Linux 4.15.0-65-generic x86_64)
        
        但依舊可以用boolean的方式判斷；不過視窗的移動，不影響mouse_over()
        if browser.is_element_present_by_xpath('//*[@id="bt_2_layout_Content"]/div[2]/ul/li[1]/a'):
            print(1)  
        """
        searchTypeList = [row for row in range(1,5)]
        pageList = [row for row in range(1,13)] # 頁碼欄的第一頁只有12項
        brandAndClassList = [row for row in range(2)]

        randomTypeNum = random.choice(searchTypeList)
        randomPageNum = random.choice(pageList)
        randomBrandClassNum = random.choice(brandAndClassList)

        try:
            try:
                # 針對頁碼，最多12項；在置底頁時，選項不會12項足項
                browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[2]/ul/li[{randomPageNum}]/a').mouse_over()
                browserWaitTime(browser)
            except AttributeError as e: # 找不到element 來mouse_over() ； 
                print("頁碼不足12項___擬人化操作找不到 Element。", e)
                browserWaitTime(browser)
            
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            timeSleepOne()
            # 針對準確度...價格等4項
            browser.find_by_xpath(f'//*[@id="bt_2_layout_Content"]/div[3]/span/ul/li[{randomTypeNum}]').mouse_over()
            timeSleepOne()
            
            #針對商標與商品分類選單
            if randomBrandClassNum:
                if browser.is_element_present_by_xpath('//*[@id="categoriesBtn"]'):
                    browser.find_by_xpath('//*[@id="categoriesBtn"]').mouse_over()
                elif browser.is_element_present_by_xpath('//*[@id="bt_0_layout_b203"]'):
                    browser.find_by_xpath('//*[@id="bt_0_layout_b203"]').mouse_over()
            else:
                if browser.is_element_present_by_xpath('//*[@id="bt_0_layout_b203"]'):
                    browser.find_by_xpath('//*[@id="bt_0_layout_b203"]').mouse_over()
                elif browser.is_element_present_by_xpath('//*[@id="categoriesBtn"]'):
                    browser.find_by_xpath('//*[@id="categoriesBtn"]').mouse_over()
                

            timeSleepOne()
            browser.execute_script('window.scrollTo(0,0);')
                
        except AttributeError as e: # 找不到element 來mouse_over() ； 
                print("擬人化操作找不到 Element。", e)



class carrefourRequests(ecommerceProductsRequests):
    
    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')

                pass 

                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()


        return 

class rtmartRequests(ecommerceProductsRequests):
    
    pass

class rakutenRequests(ecommerceProductsRequests):
    
    pass

class shapeeRequests(ecommerceProductsRequests):
    
    pass

class yahoomallRequests(ecommerceProductsRequests):
    
    pass

class etmallRequests(ecommerceProductsRequests):
    
    pass

"""

預計以類別的方式撰寫  各新聞網站的爬蟲

"""

class newsRequests(object):

    """
    設為 @classmethod 的方法內，不得使用 其他實例(self)方法
    
    """


    _headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}


    _publisherUdn = "udn聯合新聞網"

    _publisherUdnMoney = "經濟日報"

    _publisherLtn = "自由時報電子報"

    _publisherChinaTimes = "中時電子報"

    _publisherAppleDaily = "蘋果日報"

    _publisherYahoo = "Yahoo奇摩新聞"
    
    _publisherETtoday = "ETtoday"

    _publisherNOWnews = "NOWnews"

    _publisherTVBS = "TVBS新聞"


    # @classmethod
    def intersectionForCrawl(self, publisherName, newsLink):

        if not publisherName:
            videoLinkInContent, newsContent = None, None
        
        elif publisherName == self._publisherUdn:
            videoLinkInContent, newsContent = udnRequests.requests(newsLink, self._headers)
        
        elif publisherName == self._publisherUdnMoney:
            videoLinkInContent, newsContent = udnMoneyRequests.requests(newsLink, self._headers)
        
        elif publisherName == self._publisherLtn:
            videoLinkInContent, newsContent = ltnRequests.requests(newsLink, self._headers)
        
        elif publisherName == self._publisherChinaTimes:
            videoLinkInContent, newsContent = chinaTimesRequests.requests(newsLink, self._headers)
        
        elif publisherName == self._publisherAppleDaily:
            videoLinkInContent, newsContent = appleDailyRequests.requests(newsLink, self._headers)
        
        elif publisherName == self._publisherYahoo:
            videoLinkInContent, newsContent = yahooRequests.requests(newsLink, self._headers)
        
        elif publisherName == self._publisherETtoday:
            videoLinkInContent, newsContent = ettodayRequests.requests(newsLink, self._headers)
        
        elif publisherName == self._publisherNOWnews:
            videoLinkInContent, newsContent = nowNewsRequests.requests(newsLink, self._headers)
        
        elif publisherName == self._publisherTVBS:
            videoLinkInContent, newsContent = tvbsRequests.requests(newsLink, self._headers)

        return videoLinkInContent, newsContent


class udnRequests(newsRequests):

    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')
                newsContent = [textMiningRegex.discardSpace(textMiningRegex.replaceEscapeAlphabet(row.text)) 
                                    for row in soup.select_one("#story_body_content").select("p") 
                                            if row.text != ""]
                videoLinkInContent= None # 內文本身沒有影片
                break
            except AttributeError as e:

                try:
                    # 20200207 udn網頁改版
                    newsContent = [textMiningRegex.discardSpace(textMiningRegex.replaceEscapeAlphabet(row.text)) 
                                        for row in soup.find("article", {"class" : "article-content"}).find_all("p")
                                                if row.text != ""]                
                except AttributeError as e:
                    # 網頁拜訪若是404，html長的如下樣子。
                    '''
                    response404 = """<html>
                                <head>
                                <script>
                                                        var d = new Date();
                                                        d.setTime(d.getTime() + (300*1000));
                                                        var expires = "expires="+ d.toUTCString();
                                                        document.cookie = "burl=my-test-page01;" + expires + ";path=/";
                                                </script>
                                <!-- Google Tag Manager -->
                                <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
                                                new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
                                                j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
                                                'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
                                                })(window,document,'script','dataLayer','GTM-5CMHR66');</script>
                                <!-- End Google Tag Manager --><script>
                                                (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
                                                (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
                                                m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
                                                })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
                                                        </script>
                                <!-- #Location: /inc/meta/trace_ga -->
                                </head>
                                <body>
                                <!-- Google Tag Manager (noscript) -->
                                <noscript><iframe height="0" src="https://www.googletagmanager.com/ns.html?id=GTM-5CMHR66" style="display:none;visibility:hidden" width="0"></iframe></noscript>
                                <!-- End Google Tag Manager (noscript) -->
                                <script>
                                                window.location="/news/e404?nver";
                                        </script>
                                </body>
                                </html>"""
                    
                    '''

                    if searchWordTrueOrFalse("404", str(soup.select_one("body").select_one("script"))): #'<script>\n                window.location="/news/e404?nver";\n        </script>'
                        # https://udn.com/news/story/7238/3600804
                        print(url, "發生問題：404!")
                        newsContent = "404_None"
                    else:
                        # 不知名情況查看
                        print(soup)
                        newsContent = "404_None"
                        raise

                
                videoLinkInContent= None # 內文本身沒有影片
                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None

        return videoLinkInContent, newsContent

class udnMoneyRequests(newsRequests):


    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')
                newsContent = [textMiningRegex.discardSpace(textMiningRegex.replaceEscapeAlphabet(row.text))
                                    for row in soup.select_one("#article_body").select("p") 
                                            if row.text != ""]
                videoLinkInContent= None # 內文本身沒有影片

                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None

        return videoLinkInContent, newsContent

class ltnRequests(newsRequests):

    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                
                if "https://ent.ltn.com.tw/news/" in url:
                    videoLinkInContent, newsContent = ltnRequests.requestsUrlWithENT(url, headers)
                    break
                
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'lxml') # html.parser不夠力 https://ec.ltn.com.tw/article/paper/1295417 抓不到內容
                try:
                    newsContent = [textMiningRegex.discardSpace(textMiningRegex.replaceEscapeAlphabet(row.text)) 
                                        for row in soup.select_one(".text").select("p") 
                                            if row.text != ""]
                    videoLinkInContent= None # 內文本身沒有影片
                except AttributeError as e:
                    # https://news.ltn.com.tw/news/consumer/paper/1284005  --> https://ent.ltn.com.tw/news/paper/1284005
                    print("error code:", e, url)
                    videoLinkInContent, newsContent = ltnRequests.requestsUrlWithENT(url, headers)
                break

            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None

        return videoLinkInContent, newsContent

    @classmethod
    def requestsUrlWithENT(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'lxml')
                newsContent = [textMiningRegex.discardSpace(textMiningRegex.replaceEscapeAlphabet(row.text)) 
                                    for row in soup.select_one(".news_content").select("p") 
                                        if row.text != ""]
                videoLinkInContent= None # 內文本身沒有影片
                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None

        return videoLinkInContent, newsContent


class chinaTimesRequests(newsRequests):
    
    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')
                newsContent = [textMiningRegex.discardSpace(textMiningRegex.replaceEscapeAlphabet(row.text)) 
                                    for row in soup.select_one(".article-body").select("p")
                                        if row.text != ""]
                videoLinkInContent= None # 內文本身沒有影片

                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None

        return videoLinkInContent, newsContent
    
class appleDailyRequests(newsRequests):

    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')
                try:
                    newsContent = [ textMiningRegex.discardSpace(textMiningRegex.replaceEscapeAlphabet(row.text))
                                        for row in soup.select_one(".ndArticle_margin").select("p") 
                                            if row.text != ""]
                    videoLinkInContent= None # 內文本身沒有影片
                except AttributeError as e: # AttributeError: 'NoneType' object has no attribute 'select'
                    soupStr = str(soup)
                    if "<br> \xa0</p>" in soupStr:
                        # "<br> \xa0</p>"  不需要變成 "<br> \\xa0</p>"
                        """
                        sqlalchemy.exc.OperationalError: (pymssql.OperationalError) (8152, b'String or binary data would be truncated.DB-Lib error message 8152, severity 16:\nGeneral SQL Server error: Check messages from the SQL Server\n')
                        [SQL: INSERT INTO selected_news_with_tfidf ([news_title_Id], [series_Id], [publisher_Id], news_content, video_link_in_content) VALUES (%(news_title_Id)s, %(series_Id)s, %(publisher_Id)s, %(news_content)s, %(video_link_in_content)s)]
                        [parameters: {'news_title_Id': '201912252', 'series_Id': UUID('9abd7eae-c361-496c-b10c-ae9fcf7be8bb'), 'publisher_Id': '5', 'news_content': '[\'<p> 今年農曆年節時間較早，家電採購需求較以往提早出現買氣，瞄準年前有汰換家中家電的需求，大同3C福利品特賣會特於12月底開跑，一路至明年1月初，提供消費者年前採購好選擇。<br> <br> 12月26日起至2020年1月8日止，全台各地共舉辦20場大同3C福利品特賣會，大小家電可在此一次 ... 
                        (3925 characters truncated) ... aws.com/ap-ne-1-prod/public/FLCZDN5FBRQBN6E6E3S7RP7IW4.jpg","version":"0.10.3","width":640},{"_id":"IO25XHAIRJE3FCUWV7YTXI66CY","type":"raw_html",\']', 'video_link_in_content': None}]
                        (Background on this error at: http://sqlalche.me/e/e3q8)
                        """

                        # https://tw.appledaily.com/property/20191226/WCUY7RP45D2V45RLRN3RULU2QU/
                        tmpStr = soupStr.split("""<script type="application/javascript">window.Fusion=""")[1].split("Fusion.globalContent=")[1].split('"content":"')[1].split("<br> \xa0</p>")[0]
                        newsContent = [row for row in BeautifulSoup(tmpStr, "html.parser").text.split(" ") if row != ""]
                    else:
                        # https://tw.appledaily.com/gadget/20190927/IFU7ML7HXNAL2GHDNKOZULDNOU/
                        tmpStr = soupStr.split("""<script type="application/javascript">window.Fusion=""")[1].split("Fusion.globalContent=")[1].split('"content":"')[1].split("更多「")[0]
                        newsContent = [row for row in tmpStr.split("<br />&nbsp;<br />") if row != ""]

                        if len("".join(newsContent)) >= 3500:
                            # elif '<br />&nbsp;"' in soupStr:
                            # https://tw.appledaily.com/gadget/20191029/KSU3NPGRYURXTCI3COIUE6KMNM/
                            print(f"appledaily news content exceeds 3500: {url}")
                            tmpStr = soupStr.split("""<script type="application/javascript">window.Fusion=""")[1].split("Fusion.globalContent=")[1].split('"content":"')[1].split('<br />&nbsp;"}')[0]
                            newsContent = [row for row in tmpStr.split("<br />&nbsp;<br />") if row != ""]


                    videoLinkInContent= None # 內文本身沒有影片

                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None
        

        return videoLinkInContent, newsContent


class yahooRequests(newsRequests):

    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')
                try:
                    newsContent = soup.find("article",{"itemprop":"articleBody"}).text.strip().split(" ")
                except AttributeError as e:
                    # url = "https://tw.news.yahoo.com/video/%E7%AF%80%E8%83%BD%E5%AE%B6%E9%9B%BB%E8%A3%9C%E5%8A%A9%E5%86%8D%E5%8A%A0%E7%A2%BC-%E8%B2%A8%E7%89%A9%E7%A8%85%E6%B8%9B%E5%85%8D%E9%96%8B%E8%B7%91-053307068.html"
                    # print("error code:", e, url)
                    try:
                        newsContent = soup.find("article").text.strip().split(" ")
                    except AttributeError as e:
                        # "https://tw.news.yahoo.com/%E9%BB%83%E9%87%91%E9%80%B1%E5%A4%A7%E5%90%8C3c%E9%85%AC%E8%B3%93%E7%9B%9B%E5%85%B8-%E6%B6%BC%E5%A4%8F%E6%9C%80%E5%BC%B7%E6%AA%94-081101070.html": [
                        # "黃金週大同3C酬賓盛典涼夏最強檔",
                        print("error code:", "這則新聞爆炸了！", url)
                        newsContent= None


                videoLinkInContent= None # 內文本身沒有影片
                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None 

        return videoLinkInContent, newsContent

class ettodayRequests(newsRequests):

    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')
                newsContent = [row 
                                for row in soup.select_one(".story").stripped_strings]

                #內文影片
                if soup.p.iframe:#.attrs.get("src"):
                    videoLinkInContent = soup.p.iframe.attrs.get("src")
                    print("ETtoday 發現內文有影片：", videoLinkInContent)
                    
                else:
                    videoLinkInContent= None
                
                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None

        return videoLinkInContent, newsContent


class nowNewsRequests(newsRequests):

    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')
                newsContent = [textMiningRegex.discardSpace(textMiningRegex.replaceEscapeAlphabet(row.text))
                                    for row in soup.find("article").stripped_strings 
                                        if row != "" and not "googletag.cmd.push" in row and not "function"  in row ]                                        
                videoLinkInContent= None # 內文本身沒有影片
                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None

        return videoLinkInContent, newsContent


class tvbsRequests(newsRequests):

    @classmethod
    def requests(cls, url, headers):
        for i in range(3):
            try:
                timeSleepOne()
                res = requests.get(url, headers=headers)
                res.encoding = 'utf-8'
                timeSleepRandomly()

                soup = BeautifulSoup(res.text, 'html.parser')
                newsContent = ([row 
                                for row in soup.select_one(".newsdetail_content")
                                .find("div", {"class":"contxt margin_b20"})
                                .find("div", {"id":"news_detail_div"})
                                .stripped_strings])
                #內文影片
                if soup.select_one(".newsdetail_content").find("div", {"class":"contxt margin_b20"}).find("iframe", {"class":"video"}):
                    linkInContent = soup.select_one(".newsdetail_content").find("div", {"class":"contxt margin_b20"}).find("iframe", {"class":"video"}).attrs.get("src")
                    videoID = urlParseDealing.urlParsePath(linkInContent).split("/")[-1] #videoID = link.split("/embed/")[1].split("?")[0]
                    videoLinkInContent = f"https://youtube.com/watch?v={videoID}"
                    print("TVBS 發現內文有影片：", videoLinkInContent)
                    
                else:
                    videoLinkInContent= None

                
                break
            except requests.exceptions.ConnectionError as e:
                print(url, "發生問題。", e)
                print()
                timeSleepRandomly()
                timeSleepTwo()
                newsContent= None
                videoLinkInContent= None

        return videoLinkInContent, newsContent
    
        

        