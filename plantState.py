import time


class GlobalState:

    # ! plant : Plant --> pas possible d'importer ou de setup
    # ! l'IDE dectect un import circulair + class declarer avant son initialisation 
    def __init__(self, plant):
        self.plant = plant

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def afterProcess(self):
        pass

class SetupState(GlobalState):
    # Wait for all connections
    
    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def afterProcess(self):
        print("Wait for all connection")
        self.plant.waitForAllConnection()
        print("Go to StandbyAfterSetup")
        self.plant.setState(StandbyAfterSetup(self.plant))
    
    # ----------------------------------------

    def waitForAllConnection(self):
        nbConnection = 0
        while nbConnection < 4:
            print(nbConnection, "/4 sensors connected !")
            time.sleep(0.5)



class StandbyAfterSetup(GlobalState):
    # Wait for user action or pass

    def handleSwitch(self):
        print("Go to TutorielState")
        self.plant.setState(TutorielState(self.plant))

    def handleProximity(self):
        pass

    def afterProcess(self):
        print("Go to SleepState")
        self.plant.setState(SleepState(self.plant))

class TutorielState(GlobalState):
    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def afterProcess(self):
        print("Play tutorial")
        print("Go to SleepState")
        self.plant.setState(SleepState(self.plant))


class SleepState(GlobalState):
    def handleSwitch(self):
        pass

    def handleProximity(self):
        print("Go to WakeUpState")
        self.plant.setState(WakeUpState(self.plant))

    def afterProcess(self):
        pass

class WakeUpState(GlobalState):
    def handleSwitch(self):
        print("Go To AwakeState")
        self.plant.setState(AwakeState(self.plant))

    def handleProximity(self):
        pass

    def afterProcess(self):
        pass

class AwakeState(GlobalState):
    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def afterProcess(self):
        print("Go To StandbyAfterAwake")
        self.plant.setState(StandbyAfterAwake(self.plant))


class StandbyAfterAwake(GlobalState):
    # Wait for user action or pass

    def handleSwitch(self):
        print("Go to AwakeState")
        self.plant.setState(AwakeState(self.plant))

    def handleProximity(self):
        pass

    def afterProcess(self):
        print("Go to SleepState")
        self.plant.setState(SleepState(self.plant))


class Plant:

    state : GlobalState

    def __init__(self) -> None:
        self.state = SetupState(self)

    def handleSwitch(self):
        self.state.handleSwitch()

    def handleProximity(self):
        self.state.handleProximity()

    def process(self):
        self.state.afterProcess()

    def setState(self, state : GlobalState):
        self.state = state



