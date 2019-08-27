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
        print(f"創建 {dirRoute} 成功！")
    else:
        print(f"已經存在 {dirRoute} 的資料夾，不用再創建。")
        pass


def eraseCleanData(objectiveFolder, objective, searchword="", keyword=""):
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/{keyword}"
    if not os.path.isdir(dirRoute):
        print(f"沒有存在 {dirRoute} 的資料夾，因此不用清空。")
        pass
    else:
        shutil.rmtree(dirRoute)
        print(f"已經清空 {dirRoute}")

def eraseRawData(objectiveFolder, objective, searchword, keyword=""):
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolder}/{objective}/{searchword}/{keyword}"
    if not os.path.isdir(dirRoute):
        print(f"沒有存在 {dirRoute} 的資料夾，因此不用清空。")
        pass
    else:
        shutil.rmtree(dirRoute)
        print(f"已經清空 {dirRoute}")


def initialFileZeroUnderscoreInt(directory):
    readyFile = os.listdir(directory)
    readyFile.sort(key= lambda x: int(x.split('_')[0]))
    return readyFile  


def initialFileFirstUnderscoreString(directory):
    readyFile = os.listdir(directory)
    readyFile.sort(key= lambda x: x.split('_')[1])
    return readyFile

def initialFileFourthUnderscoreString(directory):
    readyFile = os.listdir(directory)
    readyFile.sort(key= lambda x: x.split('_')[4])
    return readyFile

def mkdirForCleanData(objectiveFolderClean, objective):
    dirRoute = f"{_BASE_PATH}/dataMunging/{objectiveFolderClean}/{objective}"
    if not os.path.isdir(dirRoute):
        os.mkdir(dirRoute)
        print(f"創建 {dirRoute}")
    else:
        print(f"已經存在 {dirRoute} 的資料夾")
        pass


def listSecondDirBelowFiles(dirRoute):
    """
    1. dirRoute stands for the first layor of directory:
       /home/bluevc/2019/iSelect3C/dataMunging/rawData/weather

    2. There are many folders right under the folder 『weather』, and all these folders
        contain only files instead of many other folders.

    3. if there is any files in the layor fo weather, this function will fail.

    """
    for row in os.walk(dirRoute):
        judge = 1
        if row[-1] == []: # 捕捉第二層的各資料夾
            tmpDirs = sorted(row[1])
            readyDirs = [row[0] + "/" + rowInner for rowInner in tmpDirs]
            for rawDir in readyDirs:
            # if row[-1]: #捕捉到檔案名
            #     dirRoute = row[0]
                try:
                    readyFile = initialFileZeroUnderscoreInt(rawDir)
                    for rawFile in readyFile:
                        completeName = rawDir+ "/" + rawFile
                        yield completeName
                except ValueError: #不適合用 initialFileZeroUnderscoreInt列舉的檔案
                    readyFile = os.listdir(rawDir)
                    for rawFile in readyFile:
                        completeName = rawDir+ "/" + rawFile
                        yield completeName
            judge = 0
        if not judge:
            break

#check
# for row in listSecondDirBelowFiles("/home/bluevc/2019/iSelect3C/dataMunging/rawData/news/google"):
#     print(row)
