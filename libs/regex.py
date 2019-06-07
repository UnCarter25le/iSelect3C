# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os
import sys
import re
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