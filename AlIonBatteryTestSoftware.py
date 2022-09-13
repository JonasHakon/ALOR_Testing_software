
import datetime
from math import floor
import string
import time
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
from tabulate import tabulate
import threading
from AlIonTestSoftwareDeviceDrivers import PowerSupplyController, ElectronicLoadController, MultimeterController
from AlIonTestSoftwareDeviceDriversMock import PowerSupplyControllerMock, ElectronicLoadControllerMock, MultimeterControllerMock





class TestController:

    OCVFull = 0.0

    OCVEmpty = 0.0

    C_rate = 0.0

    RunningTest = False


    def __init__(self) -> None:
        try:
            self.powerSupplyController = PowerSupplyController()
            print("Testcontroller succesfully connected to Power Supply")
            self.electronicLoadController = ElectronicLoadController()
            print("Testcontroller succesfully connected to Electronic Load")
            self.multimeterController = MultimeterController()
            print("Testcontroller succesfully connected to Multimeter")
            self.Connected = True
        except:
            print("Connection not successful, using mock objects")
            self.powerSupplyController = PowerSupplyControllerMock()
            self.electronicLoadController = ElectronicLoadControllerMock()
            self.multimeterController = MultimeterControllerMock()
            self.Connected = False

        self.event = threading.Event()


    def chargeCC(self, ampers):
        self.powerSupplyController.chargeCC(ampers)
    def chargeCV(self, volts):
        self.powerSupplyController.chargeCV(volts)
    def chargeCP(self, watts):
        self.powerSupplyController.chargeCP(watts)
    def stopCharge(self):
        self.powerSupplyController.stopCharge()
    def dischargeCC(self, amper):
        self.electronicLoadController.dischargeCC(amper)
    def dischargeCV(self, volts):
        self.electronicLoadController.dischargeCV(volts)
    def dischargeCP(self, watts):
        self.electronicLoadController.dischargeCP(watts)
    def stopDischarge(self):
        self.electronicLoadController.stopDischarge()


    def getVoltage(self):
        x = self.electronicLoadController.getVolts()
        return float(x)
    def getCurrent(self):
        return float(self.powerSupplyController.getCurrent()) - float(self.electronicLoadController.getCurrent())

    def setMaxVoltage(self, volts : int):
        self.powerSupplyController.setMaxVoltage(volts=volts)
        
    def setMaxVoltageMax(self):
        self.powerSupplyController.setMaxVoltage()
        
    def setMaxCurrent(self, amps : int):
        self.powerSupplyController.setMaxCurrent(amps=amps)

    def setMaxCurrentMax(self):
        self.powerSupplyController.setMaxCurrent()

    def setMaxPower(self, watts : int):
        self.powerSupplyController.setMaxPower(watts=watts)

    def setMaxPowerMax(self):
        self.powerSupplyController.setMaxPower()

    
    def capacityTest(self, chargeTime : int, waitTime : int, numCycles : int, CPar, temp : int):
        self.event.clear()
        self.RunningTest = True
        # Create a loop that will run one time for each element of the eather CPar or TempPar
        for cParameter in CPar: 
            # Create a list that will keep track of the estemated capacity of the battery
            ampHourCapacity = []
            # Create a loop for each cycle for the cParameter
            for cycleNumber in range(int(numCycles)): 
                dataStorage = DataStorage()
                ASeconds = 0
                # Charge with a constant voltage of self.OCVFull
                self.chargeCV(self.OCVFull)
                # Wait the desired amount of minutes
                print(f"Charging for {chargeTime} min")
                for i in range(floor(float(chargeTime) * 60)):
                    if (self.event.is_set()):
                        print("Testing has been manually stopped")
                        self.event.clear()
                        exit()
                    time.sleep(1)
                # Once the OCV has reached OCVFull we can start discharging
                self.stopCharge()
                # Wait the desired number of seconds
                print(f"Wating for {waitTime} min")
                for i in range(floor(float(waitTime) * 60)):
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    time.sleep(1)
                # Discharging at c rate current
                self.dischargeCC(self.C_rate * cParameter)
                
                # Creating a loop that will break once voltage has reached desired levels
                print(f"Starting discharge in cycle nr.{cycleNumber + 1} with discharge rate {cParameter}C")
                while (True):
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    v = self.getVoltage()
                    c = self.getCurrent()
                    dataStorage.addVoltage(v)
                    dataStorage.addCurrent(c)
                    if (float(v) < self.OCVEmpty):
                        break
                    time.sleep(1)
                    ASeconds += self.C_rate * cParameter
                self.electronicLoadController.stopDischarge()
                dataStorage.graphCapacity(cycleNumber, temp, cParameter)
                dataStorage.createTable("Capacity Test", cParameter, cycleNumber, temp )
                print(f"Capacity stored for cycle nr.{cycleNumber + 1} with C-rate of {cParameter}")
                ampHourCapacity.append([ASeconds / 3600])
            print(ampHourCapacity)
        self.RunningTest = False
        self.event.set()

    def enduranceTest(self, chargeTime : int, waitTime : int, numCycles : int, CPar, temp : int):
        self.event.clear()
        self.RunningTest = True
        # Create a loop that will run one time for each element of the eather CPar or TempPar
        for cParameter in CPar: 
            # Create a list that will keep track of the estemated capacity of the battery
            ampHourCapacity = []
            # Create a loop for each cycle for the cParameter
            for cycleNumber in range(int(numCycles)): 
                dataStorage = DataStorage()
                ASeconds = 0
                # Charge with a constant voltage of self.OCVFull
                self.chargeCV(self.OCVFull)
                # Wait the desired amount of minutes
                print(f"Charging for {chargeTime} min")
                for i in range(floor(float(chargeTime) * 60)):
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    time.sleep(1)
                # Once the OCV has reached OCVFull we can start discharging
                self.stopCharge()
                # Wait the desired number of seconds
                print(f"Wating for {waitTime} min")
                for i in range(floor(float(waitTime) * 60)):
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    time.sleep(1)
                # Discharging at c rate current
                self.dischargeCC(self.C_rate * cParameter)
                
                # Creating a loop that will break once voltage has reached desired levels
                print(f"Starting discharge in cycle nr.{cycleNumber + 1} with discharge rate {cParameter}C")
                while (True):
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    v = self.getVoltage()
                    c = self.getCurrent()
                    dataStorage.addVoltage(v)
                    dataStorage.addCurrent(c)
                    if (float(v) < self.OCVEmpty):
                        break
                    time.sleep(1)
                    ASeconds += self.C_rate * cParameter
                self.electronicLoadController.stopDischarge()
                dataStorage.createTable("Endurance Test", cParameter, cycleNumber, temp )
                
                ampHourCapacity.append([ASeconds / 3600])
            dataStorage.graphEndurance(temp, cParameter, ampHourCapacity)
            print(ampHourCapacity)
        self.RunningTest = False
        self.event.set()

            

            
class DataStorage:

    def __init__(self) -> None:
        # Empty arrays for data
        self.volts = []
        self.current = []
        self.power = []
        self.amphours = []

    #Function to add voltage value
    def addVoltage(self, votls : int):
        self.volts.append(float('{:.0f}'.format(votls)))

    #Function to add current value
    def addCurrent(self, ampers : int):
        self.current.append(float('{:.0f}'.format(ampers)))

    def createTable(self, testName : string, c_rate : float, cycleNr : int, temperature : float):
        for i in range(len(self.volts)):
            self.power.append(self.volts[i] * self.current[i])
        length = len(self.volts)
        data = [[]]
        for j in range(len(self.volts)):
            d = [j, self.volts[j], self.current[j], self.power[j]]
            data.append(d)
        head = ["Time in seconds", "Volts", "Current", "Power"]
        table = tabulate(data, headers=head, tablefmt="simple")
        print(table)  
        today = date.today() 
        with open(f"C:/Users/sirjo/Desktop/ALOR/Al-ion Battery Test Software/Data/{testName} for {c_rate}C nr. {cycleNr + 1} at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".txt", "w") as f:
            f.write(str(table))
        self.volts = []
        self.current = []
        self.power = []

    def graphCapacity(self, cyclenumber, temperature, C_rate):
        plt.style.use("ggplot")
        plt.xlabel("Time (S)")
        plt.ylabel("Voltage (V)")
        plt.title(f"Capacity at {temperature}° celsius with {C_rate} C current")
        plt.plot(range(len(self.volts)), self.volts, color = "#3a55b4")
        ahCapacity = len(self.volts) / 3600
        plt.legend([f"{'{:.2f}'.format(ahCapacity)} aH Capacity"])
        plt.savefig(f"C:/Users/sirjo/Desktop/ALOR/Al-ion Battery Test Software/Data/Capacity test for {C_rate}C nr. {cyclenumber + 1} at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".png")
        plt.clf()
        

    def graphEndurance(self, temperature, C_rate, ampHours):
        plt.style.use("ggplot")
        plt.ylabel("Capacity (Ah)")
        plt.xlabel("Cycle number")
        plt.title(f"Change in capacity at {temperature}° celsius with {C_rate} C current")
        plt.plot(range(len(ampHours)), ampHours, "o", color = "#3a55b4")
        plt.savefig(f"C:/Users/sirjo/Desktop/ALOR/Al-ion Battery Test Software/Data/Endurance test for {C_rate}C at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".png")
        plt.clf()
        


