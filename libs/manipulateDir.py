# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。
# 例如，儘管直接定義  _BASE_PATH = "/home/bluevc/2019/iSelect3C"，要是沒有import os ，也是無法執行函式mkdirForRawData。


import os
import sys
import shutil #high level os


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
# sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

def mkdirForRawData(objectiveFolder, objective, searchword, keyword=""):
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/{keyword}"
    if not os.path.isdir(dirRoute):
        os.makedirs(dirRoute)
        print(f"創建 {dirRoute}")
    else:
        print(f"已經存在 {dirRoute} 的資料夾")
        pass


def eraseRawData(objectiveFolder, objective, searchword, keyword=""):
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/{keyword}"
    if not os.path.isdir(dirRoute):
        print(f"沒有存在 {dirRoute} 的資料夾")
        pass
    else:
        shutil.rmtree(dirRoute)
        print(f"已經清空 {dirRoute}")


def initialFile(directory):
    readyFile = os.listdir(directory)
    readyFile.sort(key= lambda x: int(x.split('_')[0]))
    return readyFile  


def mkdirForCleanData(objectiveFolderClean, objective):
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}"
    if not os.path.isdir(dirRoute):
        os.mkdir(dirRoute)
        print(f"創建 {dirRoute}")
    else:
        print(f"已經存在 {dirRoute} 的資料夾")
        pass