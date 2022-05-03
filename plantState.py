import datetime
from utils.protocol import ProtocolDecodeur, ProtocolGenerator


class GlobalState:
    stateName : str

    # ! plant : Plant --> pas possible d'importer ou de setup
    # ! l'IDE dectect un import circulair + class declarer avant son initialisation 
    def __init__(self, plant):
        self.plant = plant

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def afterProcess(self):
        pass

class SetupState(GlobalState):
    # Wait for all connections

    stateName = "setup-state"

    twofa = 1

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def afterProcess(self):
        print("Wait for all connection")
        isOk = self.waitForAllConnection()
        print("isOk", isOk)
        if isOk:
            self.plant.storage.InitStorage()
            print("Go to StandbyAfterSetup after init storage !")
            self.plant.setState(StandbyAfterSetup(self.plant,10))
    
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
    stateName = "standby-after-setup"

    def __init__(self, plant,delay: int):
        super().__init__(plant)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go to TutorielState")
        self.plant.setState(TutorielState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        print("Go to SleepState")
        if (acces == self.stateName):
            self.plant.setState(SleepState(self.plant))

    def afterProcess(self):
        pass
        

class TutorielState(GlobalState):

    stateName = "tutoriel-state"

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def afterProcess(self):
        self.playTutorial()
        print("Go to SleepState")
        self.plant.setState(SleepState(self.plant))

    # ----------------------------------------

    def playTutorial(self):
        print("Play tutorial")


class SleepState(GlobalState):
    
    stateName = "sleep-state"

    def handleSwitch(self):
        pass

    def handleProximity(self):
        print("Go to WakeUpState")
        date = datetime.datetime.now()
        self.plant.storage.saveOnStore("proximity", str(date))
        self.plant.storage.saveOnFile("proximity", str(date))
        self.plant.setState(WakeUpState(self.plant, 10))

    def handleDelay(self,  acces : str):
        pass

    def afterProcess(self):
        pass

class WakeUpState(GlobalState):

    stateName = "wake-up-state"

    def __init__(self, plant,delay: int):
        super().__init__(plant)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go To AwakeState")
        self.plant.setState(AwakeState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        print("Go to SleepState")
        if (acces == self.stateName):
            self.plant.setState(SleepState(self.plant))

    def afterProcess(self):
        pass

class AwakeState(GlobalState):

    stateName = "awake-state"

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def afterProcess(self):
        print("Go To StandbyAfterAwake")
        print("Systeme/Miror/jsp")
        self.plant.setState(StandbyAfterAwake(self.plant, 10))


class StandbyAfterAwake(GlobalState):

    stateName = "standby-after-awake"
    
    def __init__(self, plant,delay: int):
        super().__init__(plant)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go to AwakeState")
        self.plant.setState(AwakeState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        print("Go to SleepState")
        if (acces == self.stateName):
            self.plant.setState(SleepState(self.plant))

    def afterProcess(self):
        pass


