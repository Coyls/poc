import RPi.GPIO as GPIO
import time
from websocket import create_connection
from protocol import ProtocolGenerator
 
SENSOR_PIN = 23
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# time.sleep(2)

ws = create_connection("ws://localhost:8000")
 
def my_callback(channel):
    data = ProtocolGenerator("/proximity", "1")
    ws.send(data.create())
    print('There was a movement!')
 
try:
    time.sleep(5)
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=my_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("Finish...")

GPIO.cleanup()