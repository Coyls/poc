from typing import List
from utils.protocol import DbLineGenerator
dbPath = './db/db.txt'


def getIndexKey(key: str, lines: List[str]):
    for i, line in enumerate(lines):
        if key in line:
            return i
    return False

def getLines():
    f = open(dbPath, "r")
    lines = f.readlines()
    f.close()
    return lines

def modifyLines(lines: List[str],data: str, index):
    lines[index] = data if index else lines.append(data)
    return lines

def createLines(lines):
    w = open(dbPath, "w")
    w.writelines(lines)
    w.close()

def addValue(key: str, data: str):
    lines = getLines()
    index = getIndexKey(key, lines)
    rawData = DbLineGenerator(key,data)
    dataRdyToUse = rawData.create()
    lines = modifyLines(lines, dataRdyToUse, index)
    createLines(lines)
    print(lines)



addValue('switch', "data")

