from simple_websocket_server import WebSocketServer, WebSocket
from protocol import ProtocolDecodeur
from datetime import date, datetime, time
import subprocess

class Sensor:
    value = 0
    lastTrigger = datetime(2000,1,1)

    def __init__(self, delta : int, filePath :str ):
        self.delta = delta

        file = open(filePath, "r")
        lastTrigger = file.readline()
        print(lastTrigger)
        if lastTrigger != "":
            self.lastTrigger = datetime.strptime(lastTrigger, '%Y-%m-%d %H:%M:%S.%f')


    def setValue(self, val : int):
        self.value = val
        self.setLastActivation()
    
    def setLastActivation(self):
        print("Set last trigger : ", datetime.now())
        file = open("last-trigger.txt", "w")
        file.write(f"{datetime.now()}")
        self.lastTrigger = datetime.now()

    def canActivate(self) -> bool:
        now = datetime.now()
        res = now - self.lastTrigger
        print("Total Second : ", int(res.total_seconds()))
        return True if res.total_seconds() >= self.delta else False

class Storage:
    proximity = Sensor(100, "empty.txt")
    temp = Sensor(10, "empty.txt")
    switch = Sensor(10,"empty.txt")
    humidityGround = Sensor(10, "last-trigger.txt")

    def setValue(self, key: str, val: str):
        if key == "/temp":
            self.temp.setValue(int(val))
        if key == "/proximity":
            if self.proximity.canActivate():
                self.proximity.setValue(int(val))
                subprocess.run(['espeak','-vfr+f4','-s150', "Bonjour, Humain !"])
        if key == "/switch":
            self.switch.setValue(int(val))
        if key == "/humidity-ground":
            self.humidityGround.setValue(int(val))
            subprocess.run(['espeak','-vfr+f4','-s150', "Merci Humain !"])
            
        
class Command:

    def __init__(self, cmd: str) -> None:
        self.cmd = cmd

    def use(self):
        return subprocess.run(self.cmd.split(" "))



class Hub:

    storage = Storage()

    def handle(self, data : str):
        dataTr = ProtocolDecodeur(data)
        [key, val] = dataTr.getKeyValue()
        self.storage.setValue(key, val)       

        if key == "/switch" and self.storage.proximity.value == 1:
            lastWatering = self.storage.proximity.lastTrigger
            last = f"La plante à été aroser pour la derniere fois le {lastWatering.day}, {lastWatering.month} à {lastWatering.hour} heures et {lastWatering.minute} minutes."
            subprocess.run(['espeak','-vfr+f4','-s150',f"la temperature est de {self.storage.temp.value} degré"])
            subprocess.run(['espeak','-vfr+f4','-s150', last])
            print(last)
            time.sleep(2)

            



class SimpleChat(WebSocket):

    hub = Hub()

    def handle(self):
        self.hub.handle(self.data)
        
    def connected(self):
        clients.append(self)
        print(self.address, 'connected')

    def handle_close(self):
        clients.remove(self)
        print(self.address, 'closed')
        
clients = []

server = WebSocketServer('', 8000, SimpleChat)
server.serve_forever()
