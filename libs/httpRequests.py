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
                        urlParseDealing
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
                    # https://tw.appledaily.com/gadget/20190927/IFU7ML7HXNAL2GHDNKOZULDNOU/
                    tmpStr = str(soup).split("""<script type="application/javascript">window.Fusion=""")[1].split("Fusion.globalContent=")[1].split('"content":"')[1].split("更多「")[0]
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
                    print("error code:", e, url)
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
                                    for row in soup.find("span", {"itemprop":"articleBody"}).select("p") 
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
    
        

        