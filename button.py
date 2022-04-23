from websocket import create_connection
import RPi.GPIO as GPIO
import time
from protocol import ProtocolGenerator

class Button:
    SENSOR_PIN = 12

    def __init__(self, name : str, data : str) -> None:
        self.name = name
        self.data = data
        self.ws = create_connection("ws://localhost:8000")
        time.sleep(3)
        self.setupHardware()
        self.initName()
    
    def start(self):
        while True:
            print(self.name , " is working !")
            time.sleep(10)

    def initName(self):
        data = ProtocolGenerator("/name", self.name)
        self.ws.send(data.create())

    def setupHardware(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.SENSOR_PIN, GPIO.RISING, callback=self.sensor_callback)

    def sensor_callback(self,channel):
        print('==============')
        print("button pushed")
        print("Sending data")
        data = ProtocolGenerator("/button", self.data)
        self.ws.send(data.create())
        print('==============')


btn = Button("Button", "1")
btn.start()


