from typing import Any
from plantState import GlobalState, SetupState, StandbyAfterSetup, TutorielState, SleepState, WakeUpState, AwakeState, StandbyAfterAwake
from simple_websocket_server import WebSocketServer
# from server import SensorConnection, ConnectionManager

class Plant:

    state : GlobalState

    def __init__(self) -> None:
        self.state = SetupState(self)
        print("New Instance")

    """ def rooting(self, client: Any):
        pass """

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