from utils.protocol import DbLineGenerator


class FileManager:
    def __init__(self, filePath:str) -> None:
        self.filePath = filePath

    def createFile(self):
        f = open(self.filePath, "w")
        f.close()

    def getLines(self) -> list[str]:
        f = open(self.filePath, "r")
        lines = f.readlines()
        f.close()
        return lines

    def getIndexKey(key: str, lines: list[str]):
        for i, line in enumerate(lines):
            if key in line:
                return i
        return False
    
    def modifyLines(self,lines: list[str],data: str, index):
        lines[index] = data if index else lines.append(data)
        return lines

    def createLines(self,lines):
        w = open(self.filePath, "w")
        w.writelines(lines)
        w.close()

    def addValue(self,key: str, data: str):
        lines = self.getLines()
        index = self.getIndexKey(key, lines)
        rawData = DbLineGenerator(key,data)
        dataRdyToUse = rawData.create()
        lines = self.modifyLines(lines, dataRdyToUse, index)
        self.createLines(lines)
        print(lines)