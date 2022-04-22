#!/usr/bin/python
from tkinter import W
import RPi.GPIO as GPIO
import time
from websocket import create_connection
from protocol import ProtocolGenerator


#GPIO SETUP
channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

# time.sleep(2)

ws = create_connection("ws://localhost:8000")

time.sleep(2)

def callback(channel):
        data = ProtocolGenerator("/humidity-ground", "1")
        rdyToSend = data.create()
        if GPIO.input(channel):
                print("Water Detected!")
                ws.send(rdyToSend)
        else:
                print("Water Detected!")
                ws.send(rdyToSend)
 
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
 
# infinite loop
while True:
        time.sleep(10)