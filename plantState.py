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
    twofa = 1

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def afterProcess(self):
        print("Wait for all connection")
        isOk = self.waitForAllConnection()
        print("isOk", isOk)
        if isOk:
            print("Go to StandbyAfterSetup")
            self.plant.setState(StandbyAfterSetup(self.plant,30))
    
    # ----------------------------------------

    def waitForAllConnection(self) -> bool:
        nb = len(self.plant.connectionManager.clients)
        
        if (nb >= 3 and self.twofa >= 3):
            return True
        else:
            self.twofa += 1
            return False
        

class StandbyAfterSetup(GlobalState):
    # Wait for user action or pass

    def __init__(self, plant,delay: int):
        super().__init__(plant)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        cl.send_message(str(self.delay))

    def handleSwitch(self):
        print("Go to TutorielState")
        self.plant.setState(TutorielState(self.plant))

    def handleProximity(self):
        pass

    def afterProcess(self):
        # print(self.plant.storage.createStore())
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




