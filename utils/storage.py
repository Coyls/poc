from utils.connectionManager import ConnectionManager
from utils.fileManager import FileManager
from utils.protocol import DbLineDecodeur

class Storage:
    store : dict[str, str] = {}
    notStored = ["eureka", "button"]
    fileManager = FileManager('./db/db.txt')

    def __init__(self, connectionManager : ConnectionManager):
        self.connectionManager = connectionManager

    def InitStorage(self):
        self.createFile()
        self.createStore()
        self.InitValueStore()

    def InitValueStore(self):
        lines = self.fileManager.getLines()
        for line in lines:
            l = DbLineDecodeur(line)
            [key, val] = l.getKeyValue()
            self.store[key] = val
        print(self.store)
        
    def createStore(self):
        cl = self.connectionManager.clients
        for key, value in cl.items():
            if value in self.notStored:
                pass
            else:
                self.store[value] = ""
        print(self.store)

    def createFile(self):
        self.fileManager.createFile()

    def saveOnFile(self, key:str, data:str):
        self.fileManager.addValue(key, data)

    def saveOnStore(self, key:str, data:str):
        self.store[key] = data