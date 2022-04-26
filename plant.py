from typing import Any
from plantState import GlobalState, SetupState, StandbyAfterSetup, TutorielState, SleepState, WakeUpState, AwakeState, StandbyAfterAwake
from simple_websocket_server import WebSocket

from protocol import ProtocolDecodeur

class ConnectionManager:
    clients : dict[WebSocket, str] = {}
    discClients : list[str] = []

    def addClient(self,client : WebSocket):
        print(client.address, 'connected')
        self.clients[client] = ""

    def setClientName(self,client : WebSocket, name : str):
        self.clients[client] = name

    def removeClient(self,client : WebSocket):
        print(client.address, 'closed')
        print(self.clients[client], " disconnected")
        self.discClients.append(self.clients[client])
        self.clients.pop(client)

# !! PAS FINI
class Storage:
    store : dict[str,dict[str,Any]]

    def __init__(self, connectionManager : ConnectionManager):
        self.connectionManager = connectionManager

    def createStore(self):
        print("createStore : ",self.connectionManager.clients)
        
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
            self.process()
            print(self.state)

        if key == "/switch":
            self.handleSwitch()
            print("/switch : ",self.state)

        if key == "/proximity":
            self.handleProximity()
            print("/proximity : ",self.state)

        if key == "/humidity-ground":
            print(key ," : ", val)
        
        if key == "/temperature":
            print(key ," : ", val)

        if key == "/button":
            print(key ," : ", val)
        