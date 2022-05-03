import datetime
from typing import Any
from plantState import GlobalState, SetupState
from simple_websocket_server import WebSocket
from utils.connectionManager import ConnectionManager
from utils.protocol import ProtocolDecodeur
from utils.storage import Storage

class Plant:

    state : GlobalState
    connectionManager = ConnectionManager()
    storage : Storage

    def __init__(self):
        self.state = SetupState(self)
        self.storage = Storage(self.connectionManager)

    def handle(self, client : WebSocket):
        self.rooter(client)

    def handleSwitch(self):
        self.state.handleSwitch()

    def handleProximity(self):
        self.state.handleProximity()

    def handleDelay(self, stateName : str):
        self.state.handleDelay(stateName)

    def process(self):
        self.state.afterProcess()

    def setState(self, state : GlobalState):
        self.state = state

    def decodeData(self, data : str) -> list[str]:
        dataTr = ProtocolDecodeur(data)
        return dataTr.getKeyValue()

    def rooter(self, client : WebSocket):
        [key, val] = self.decodeData(client.data)

        if key == "/name":
            self.connectionManager.setClientName(client,val)
            print(val, " add to clients")
            self.process()
            print(self.state)

        if key == "/eureka":
            self.handleDelay(val)
            print("/eureka : ",self.state)

        if key == "/switch":
            self.handleSwitch()
            print("/switch : ",self.state)

        if key == "/proximity":
            self.handleProximity()
            print("/proximity : ",self.state)

        if key == "/humidity-ground":
            print(key ,":", val)
            self.storage.saveOnFile(key, str(datetime.datetime.now()))
            self.storage.saveOnStore(key, str(datetime.datetime.now()))
        
        if key == "/temperature":
            print(key ,":", val)
            self.storage.saveOnStore(key, val)

        if key == "/button":
            print(key ,":", val)
        