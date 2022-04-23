from websocket import create_connection
import RPi.GPIO as GPIO
import dht11
import time
import math
from protocol import ProtocolGenerator



""" GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)

ws = create_connection("ws://localhost:8000")

time.sleep(3)

name = ProtocolGenerator("/name", "temperature")

ws.send(name.create())

while True:
    result = instance.read()
    tmp = str(math.ceil(float(f"{result.temperature}")))
    hum = str(math.ceil(float(f"{result.humidity}")))
    data = ProtocolGenerator("/temp",tmp)
    if tmp == "0":
        continue
    print(data.create())
    ws.send(data.create())
    time.sleep(3) """


class TemperatureSensor:
    SENSOR_PIN = 14

    def __init__(self, name : str) -> None:
        self.name = name
        self.instance = dht11.DHT11(self.SENSOR_PIN)
        self.ws = create_connection("ws://localhost:8000")
        time.sleep(3)
        self.setupHardware()
        self.initName()
    
    def start(self):
        while True:
            print(self.name , " is working !")
            tmp = self.getTemp()
            self.sendTemp(tmp)
            time.sleep(10)

    def initName(self):
        data = ProtocolGenerator("/name", self.name)
        self.ws.send(data.create())

    def setupHardware(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

    def getTemp(self) -> str:
        tmp = "0"
        while tmp == "0":
            result = self.instance.read()
            tmp = str(math.ceil(float(f"{result.temperature}")))
            # hum = str(math.ceil(float(f"{result.humidity}")))
        return tmp

    def sendTemp(self, tmp : str):
        data = ProtocolGenerator("/temp",tmp)
        self.ws.send(data.create())


tmp = TemperatureSensor("Temperature")
tmp.start()