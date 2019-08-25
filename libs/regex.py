# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os
import sys
import re
import sre_constants
import random
from math import ceil

_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
# sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module


def searchNums(bookurl):
    searchNum = re.compile('\d+')
    number = searchNum.search(bookurl).group()
    return number

def interDiv(Anum,Bnum):
    totalPage = ceil(int(searchNums(Anum)) / Bnum)
    return totalPage


def searchFloatNums(bookurl):
    searchNum = re.compile('\d+\.*\d*')
    number = searchNum.search(bookurl).group()
    return number

def floatDiv(Anum,Bnum):
    A = float(searchFloatNums(Anum))
    B = float(searchFloatNums(Bnum))
    return round(A / B,2)


def discardSpace(word):
    return word.replace(" ","")


def randomChoice(arrayList):
    return random.choice(arrayList)

def searchWordTrueOrFalse(regexword, wordsComparison):
    # print(regexword)
    # 如果 regexword="(" or ")" ，compile會報錯 re_constants.error: missing ), unterminated subpattern at position 0 ；unbalanced parenthesis at position 0
    # 如果 regexword="?" 會報錯：sre_constants.error: nothing to repeat at position 0   ，因為「?」的意思是前面的字元出現0~1次

    # 此商品型號放進re裡面，報錯 sre_constants.error: bad escape \V at position 18
    # 12791＋CGWLUX301GAIALTRCI\Vr00(NG1
    # https://ranking.energylabel.org.tw/product/Approval/upt.aspx?pageno=240&key2=&key=&con=0&pprovedateA=&pprovedateB=&approvedateA=&approvedateB=&Type=45&comp=0&RANK=0&refreA=0&refreB=0&condiA=0&condiB=0&HDA=0&HDB=0&SWHA=0&SWHB=0&p0=51335&id=12791#    
    
    try:
        searchwrod = re.compile(f"{regexword}")
        searchResult = searchwrod.search(wordsComparison)
        if searchResult:
            return 1
        else:
            return 0
    except sre_constants.error as e:
        print(f"「{regexword}」 has error code:", e)
        # raise
        return 0

def searchWordStartAndEnd(regexword, wordsComparison):
    
    
    searchwrod = re.compile(f"{regexword}")
    searchResult = searchwrod.search(wordsComparison)
    
    return searchResult.start()
    

def fullMatchWordTrueOrFalse(regexword, wordsComparison):

    try:
        fullMatchwrod = re.compile(f"{regexword}")
        fullMatchResult = fullMatchwrod.fullmatch(wordsComparison)
        if fullMatchResult:
            return 1
        else:
            return 0
    except sre_constants.error as e:
        print(f"「{regexword}」 has error code:", e)
        # raise
        return 0

class textMiningRegex(object):
    def sanitize(self, txt):
        # 保留英數字, 中文 (\u4e00-\u9fa5) 及中文標點, 部分特殊符號
        # http://ubuntu-rubyonrails.blogspot.com/2009/06/unicode.html
        expr = re.compile('[^\u4e00-\u9fa5。；，：“”（）、？「」『』【】\s\w:/\-.()]')  # ^ 表示"非括號內指定的字元"
        txt = re.sub(expr, '', txt)
        txt = re.sub('[。；，：“”（）、？「」『』【】:/\-_.()]', ' ', txt)  # 用空白取代中英文標點
        txt = re.sub('(\s)+', ' ', txt)  # 用單一空白取代多個換行或 tab 符號
        txt = txt.replace('--', '')
        txt = txt.lower()  # 英文字轉為小寫
        return txt


class bureauEnergyReplace(object):
    def productModel(self, product_model):
        """
        一定得做這樣的處理，否則overview and detail的product model在比對時，會出錯。
        """
        return product_model.replace("\n","").replace(" ","")

    def capacity(self, capacity):
        return capacity.replace("公升", " L").replace('\t','')

    def capacityDay(self, capacity):
        return capacity.replace("公升/日", " L/day")
    
    def capacityHour(self, capacity):
        return capacity.replace("公升/千瓦小時公升", " L/kWh")

    def capacityHourSpecial(self, capacity):
        return capacity.replace("公升/千瓦小時", "L/kWh")

    def capacityMonth(self, capacity):
        return capacity.replace("公升/度/月", " L/kWh/month")

    def capacityMonthSpecial(self, capacity):
        return capacity.replace("公升/度/月", "L/kWh/month")        

    def est24(self, est24):
        return est24.replace("(kWh/24小時)", " kWh/24hr")

    def est24Special(self, est24):
        return est24.replace("Est,24 (度，kWh)", "kWh/24hr")

    def date(self, date):
        return date.replace('/','-')

    def categoryExtract(self, category):
        searchCategory = re.compile("\([A-Z0-9]+\)")
        category = searchCategory.search(category).group()
        return category  # "LP-T228(NG1)"   --->  (NG1)

    def productModelExtract(self, productModel):
        if not "/" in productModel:
            searchProductModel = re.compile("[a-zA-Z0-9-]+")
            productModel = searchProductModel.search(productModel).group()
            # "旺旺LP-CH-903(110V)"  ---> LP-CH-903
        else:
            searchProductModel = re.compile("[a-zA-Z0-9-/]+")
            productModel = searchProductModel.search(productModel).group()
            # E/7303GAIAL2TR(NG1)  ---> E/7303GAIAL2TR
        return productModel 

    def productModelExtractAdvanced(self, productModel):
        # 避免這種情況 ："櫻花牌--SH-1335--13公升恆溫強制排氣熱水器(部分地區含基本安裝)"
        # ---> "SH-1335"
        try:
        # 只比對以「-」相連的型號，如「SH-1335-A23d」
            searchProductModel = re.compile("[a-zA-Z0-9]+-?[a-zA-Z0-9]+-?[a-zA-Z0-9]+-?[a-zA-Z0-9]+-?[a-zA-Z0-9]+")
            productModel = searchProductModel.search(productModel).group()    
        except AttributeError as e:
        # 型號沒有一槓 ：SD20
            searchProductModel = re.compile("[a-zA-Z0-9]+")
            productModel = searchProductModel.search(productModel).group()    
        return productModel 
    

    def productNameExtract(self, productName):
        seachBrandName = re.compile("[a-zA-Z]+")
        remainingName = seachBrandName.sub("", productName)

        searchProductModel = re.compile("[a-zA-Z0-9-/ ]{5,100}")
        try:
            productModel = searchProductModel.search(remainingName).group()
        except AttributeError as e:
            productModel = "nothingBeFound"
        return productModel



class numsHandler(object):
    def searchNums(self, bookurl):
        searchNum = re.compile('\d+')
        number = searchNum.search(bookurl).group()
        return number

    def interDiv(self, Anum, Bnum):
        totalPage = ceil(int(searchNums(Anum)) / Bnum)
        return totalPage

    @classmethod
    def searchFloatNums(cls, bookurl):
        searchNum = re.compile('\d+\.*\d*')
        number = searchNum.search(bookurl).group()
        return number


    def floatDiv(self, Anum, Bnum):

        A = float(numsHandler.searchFloatNums(Anum))
        B = float(numsHandler.searchFloatNums(Bnum))
        return round(A / B,2)

    
# searchwrod = re.compile("udn.com")
# searchResult = searchwrod.search("https://tw.appledaily.com/new/realtime/20190611/1579099/")
# searchResult = searchwrod.search("https://udn.com/news/story/11319/3903974")
# searchwrod = re.compile("\s+")
# searchResult = searchwrod.search("1 23")
# print(searchResult)

# aa = numsHandler()
# print(aa.floatDiv("102.1" , "209"))
# aa = "LP-T228(NG1)"
# aa = "天然氣(NG1)"
# print(re.search("\([A-Z0-9]+\)", aa).group())

# aa = "最低能源效率基準：1.09 Est,24 (度，kWh)".replace("Est,24 (度，kWh)", "kWh/24hr")
# print(aa)
# aa = "LP-CH-906A(220V)附RO逆滲透純水機"
# aa = "LP-CH-903(110V)"
# print(re.match( "[a-zA-Z0-9-]+", aa).group())
# print(re.search( "[a-zA-Z0-9-]+", aa).group())
# aa = "QB R 80 V 2,5K TW ".replace(" ","")
# aa = "UR-9615AG-110V".replace("-220V", "")
# print(re.search( "[a-zA-Z0-9-]+", aa).group())


# # aa = "國際牌14.5坪頂級LJ系列R32冷媒變頻單冷分離式CS-LJ90BA2/CU-LJ90BCA2"
# aa = "【SAMPO聲寶】5-7坪變頻右吹窗型冷氣AW-PC36D"
# # aa = "【中古】Panasonic エアコンリモコン ACXA75C13980"
# # aa = "德國 JJPRO 7000BTU(3坪 移動式冷氣/空調 (冷氣/風扇/除濕/乾衣 四機和一 JPP05)"
# # aa = "【奇美CHIMEI】7-9坪極光系列變頻冷暖一對一分離式空調RB-S50HF1/ RC-S50HF1"
# # aa = "【hokua北陸】Wu Wen Pan+ 名廚聯名炒鍋(瓦斯爐專用) 24cm"
# aaa = re.compile("[a-zA-Z]+")

# aa = "莊頭北 TH-5127RF 加強抗風12L屋外型熱水器"
# bb = aaa.sub("" ,aa, count=1) # count= 只取代幾次
# print(bb)
# # HERAN
# print(bb)
# # aa = "MAXE萬士益 MVH系列變頻冷暖一對一分離式空調 RA-50MVH/MAS-50MVH"
# # aa = "德國 JJPRO 7000BTU(3坪 移動式冷氣/空調 (冷氣/風扇/除濕/乾衣 四機和一 JPP05)"

# try:
#     # print(re.search( "[a-zA-Z0-9-/ ]{5,100}", bb).group())
#     dd = re.search( "[a-zA-Z0-9-/ ]{5,100}", bb).group()
#     cc = (r for r in dd.split("/"))
#     # print(dd)
#     for r in cc:
#         print(r)
# except AttributeError as e:
#     print("nothingFound")



# print(searchWordTrueOrFalse("PH-1215FE", "PH-1215FEA"))



# gg = re.search("SH-1335", "櫻花SAKURA 數位恆溫13L強制排氣型熱水器 SH-1335桶裝瓦斯")
# # gg = re.search("CS-LJ90", "分離式CS-LJ90BA2/CU-LJ90BCA2")
# print(gg.start())
# # 避免start後，name變成這樣「SH-1335桶裝瓦斯」，所以在用re比對一次，變成「SH-1335」
# print(bureauEnergyReplace().productModelExtract("櫻花SAKURA 數位恆溫13L強制排氣型熱水器 SH-1335桶裝瓦斯"[25:]).split("/"))


# "櫻花牌--SH-1335--13公升恆溫強制排氣熱水器(部分地區含基本安裝)"
# gg = re.search("SH-1335", "櫻花牌--SH-1335--13公升恆溫強制排氣熱水器(部分地區含基本安裝)")
# print(gg.start())
# print(bureauEnergyReplace().productModelExtractAdvanced("SD20"))
# print(bureauEnergyReplace().productModelExtractAdvanced("SH-1335--"))
# print(bureauEnergyReplace().productModelExtractAdvanced("櫻花牌--SH-1335-D3 13公升----13公升恆溫強制排氣熱水器(部分地區含基本安裝)"))
# "【Frigidaire 富及第】11L 超靜音節能除濕機 FDH-1111KA 5-7坪"
# print(bureauEnergyReplace().productModelExtractAdvanced("節能除濕機 FDH-1111KA 5-7坪"))

# print(bureauEnergyReplace().productModelExtractAdvanced("LC-060I SPA-ZA WHALE LIGHT "))
# print(re.search("[ 0-9]+", "SH-13 35--13公升恆溫強制排氣熱水器(部分地區含基本安裝)").group())
# aa = "E/730 3G AI AL 2TR"
# aa = "E/7303GAIAL2TR(NG1)"
# print(bureauEnergyReplace().productModelExtract(aa))

# print(re.search("[a-zA-Z0-9-/]+", aa).group())

# aa = "FLE20TBX/827/E27120V"
# aa = "FSL21L-EX120/T3"
# print(bureauEnergyReplace().productModelExtract(aa))