# -*- coding:utf-8 -*-

"""
程式名稱：
程式描述：


備　　註：

    

"""
import os
import sys
import json
from collections import Counter
_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)




if __name__ == '__main__':
    objectiveFolder = "rawData"

    objective = "news"

    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/newsIntegration"

    fileName = os.listdir(dirRoute).pop()

    counterNum = Counter()

    with open(dirRoute + "/" + fileName)as f:
        inn = json.load(f)

    countNum = Counter()

    for key in inn['newsUrl']:
        newsword = inn['newsUrl'][key][1]
        if newsword in countNum:
            countNum[newsword] += 1
        else:
            countNum[newsword] = 1

    print(countNum.most_common(50))
