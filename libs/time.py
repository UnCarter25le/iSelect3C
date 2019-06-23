# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。
# 例如 def timeSleepEight被引用，那麼其中的time模組就必須在這裡 import。

import os
import sys
import time
import random
import datetime


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module
from libs.regex import searchNums


def timeCalculate():
    return time.time()


def timeSleepEight():
    time.sleep(8)


def timeSleepFour():
    time.sleep(4)

def timeSleepThree():
    time.sleep(3)

def timeSleepTwo():
    time.sleep(2)

def timeSleepOne():
    time.sleep(1)


def timeSleepRandomly():
    time.sleep(random.choice([2.6, 2.9, 1.8 ,2.8, 3.1, 1.5, 3.4, 4.1, 3.6]))


def timeStampGenerator():
    dateTime = datetime.datetime.now()
    fmt = "%Y-%m-%d-%H-%M"  #"%Y年%m月%d日%H時%M分"
    timeStamp = dateTime.strftime(fmt)
    return timeStamp



# 新聞發布的時間情況
# 9 小時前
# 5 小時前
# 27 分鐘前
def timeStampCalculate(hoursOrMinutesAgo):
    timeList = timeStampGenerator().split("-")[:-2]
    if "小時" in hoursOrMinutesAgo:
        # programInitialHour = timeList[-2]
        # newsHour = str(int(programInitialHour) - int(searchNums(hoursOrMinutesAgo)))
        # timeList[-2] = newsHour
        return "-".join(timeList)
    elif "分鐘" in hoursOrMinutesAgo: # 一律以開始hour扣除1個小時
        # programInitialHour = timeList[-2]
        # newsHour = str(int(programInitialHour) - 1)
        # timeList[-2] = newsHour
        return "-".join(timeList)
    else:
        strfTime = hoursOrMinutesAgo.replace("年","-").replace("月","-").replace("日","")
        fmt = "%Y-%m-%d"  #"%Y年%m月%d日"
        return datetime.datetime.strptime(strfTime, fmt).date().__str__()