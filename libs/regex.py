# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os
import sys
import re
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
    # 如果 regexword="(" or ")" ，compile會報錯 re_constants.error: missing ), unterminated subpattern at position 0 ；unbalanced parenthesis at position 0
    
    searchwrod = re.compile(f"{regexword}")
    searchResult = searchwrod.search(wordsComparison)
    if searchResult:
        return 1
    else:
        return 0



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

    

searchwrod = re.compile("\s+")
searchResult = searchwrod.search("1 23")
print(searchResult.start())

aa = numsHandler()
print(aa.floatDiv("102.1" , "209"))
aa = "LP-T228(NG1)"
aa = "天然氣(NG1)"
print(re.search("\([A-Z0-9]+\)", aa).group())

# aa = "最低能源效率基準：1.09 Est,24 (度，kWh)".replace("Est,24 (度，kWh)", "kWh/24hr")
# print(aa)
# aa = "LP-CH-906A(220V)附RO逆滲透純水機"
# aa = "LP-CH-903(110V)"
# print(re.match( "[a-zA-Z0-9-]+", aa).group())
# aa = "QB R 80 V 2,5K TW ".replace(" ","")
# aa = "UR-9615AG-110V".replace("-220V", "")
# print(re.search( "[a-zA-Z0-9-]+", aa).group())


# def sanitize(txt):
#     # 保留英數字, 中文 (\u4e00-\u9fa5) 及中文標點, 部分特殊符號
#     # http://ubuntu-rubyonrails.blogspot.com/2009/06/unicode.html
#     expr = re.compile('[^\u4e00-\u9fa5。；，：“”（）、？「」『』【】\s\w:/\-.()]')  # ^ 表示"非括號內指定的字元"
#     txt = re.sub(expr, '', txt)
#     txt = re.sub('[。；，：“”（）、？「」『』【】:/\-_.()]', ' ', txt)  # 用空白取代中英文標點
#     txt = re.sub('(\s)+', ' ', txt)  # 用單一空白取代多個換行或 tab 符號
#     txt = txt.replace('--', '')
#     txt = txt.lower()  # 英文字轉為小寫
#     return txt

