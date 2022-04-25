from typing import Any
from plantState import GlobalState, SetupState, StandbyAfterSetup, TutorielState, SleepState, WakeUpState, AwakeState, StandbyAfterAwake
from simple_websocket_server import WebSocket

from protocol import ProtocolDecodeur

class ConnectionManager:
    clients = {}
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
        

class Plant:

    state : GlobalState
    connectionManager = ConnectionManager()

    def __init__(self) -> None:
        self.state = SetupState(self)

    def start(self, client : WebSocket):
        self.handleProximity()
        self.handleSwitch()
        self.process()
        print(self.state)

    def handle(self, client : WebSocket):
        dataTr = ProtocolDecodeur(client.data)
        [key, val] = dataTr.getKeyValue()

        if key == "/name":
            print(key , val)
            self.connectionManager.setClientName(client,val)

            print("Data received !")


    def handleSwitch(self):
        self.state.handleSwitch()

    def handleProximity(self):
        self.state.handleProximity()

    def process(self):
        self.state.afterProcess()

    def setState(self, state : GlobalState):
        self.state = state

    


""" plant = Plant()
pl = Plant()


print(plant == pl) """

""" plt = Plant()

print(plt.state)
plt.process()

print(plt.state)

plt.handleSwitch()

print(plt.state) """