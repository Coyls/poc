# Eurêka
import websocket
import RPi.GPIO as GPIO
import time
from protocol import ProtocolGenerator

class Eureka:

    def __init__(self, name : str, data : str) -> None:
        self.name = name
        self.data = data
        
    def start(self,ws):
        self.initName(ws)

    def initName(self, ws):
        data = ProtocolGenerator("name", self.name)
        ws.send(data.create())

erk = Eureka("eureka", "1")

def on_message(ws, message):
    print("Delai de ", message, " second !")
    delay = int(message)
    time.sleep(delay)
    print("Send after delay")
    data = ProtocolGenerator(erk.name, "1")
    ws.send(data.create())

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    erk.start(ws)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000", on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)

    ws.run_forever() 

    
    
