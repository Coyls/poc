import sys
from websocket import create_connection
import RPi.GPIO as GPIO
import dht11
import time
import math
import sys
from protocol import ProtocolGenerator

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)

ws = create_connection("ws://localhost:8000")

time.sleep(3)

while True:
    result = instance.read()
    tmp = str(math.ceil(float(f"{result.temperature}")))
    hum = str(math.ceil(float(f"{result.humidity}")))
    data = ProtocolGenerator("/temp",tmp)
    if tmp == "0":
        continue
    print(data.create())
    ws.send(data.create())
    time.sleep(60)
