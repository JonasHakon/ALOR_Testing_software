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
import os




# Class used to control test procedures
class TestController:
    # Variable for keeping track of the open circuit voltage of a full battery
    OCVFull = 0.0
    # Variable for keeping track of the open circuit voltage of a empty battery
    OCVEmpty = 0.0
    # Variable for keeping track of the C-rate of the battery
    C_rate = 0.0

    # Initiating function
    def __init__(self) -> None:
        try:
            # Trying to connect to the real device controllers
            self.powerSupplyController = PowerSupplyController()
            print("Testcontroller succesfully connected to Power Supply")
            self.electronicLoadController = ElectronicLoadController()
            print("Testcontroller succesfully connected to Electronic Load")
            self.multimeterController = MultimeterController()
            print("Testcontroller succesfully connected to Multimeter")
        except:
            # Connecting to the mock device controllers
            print("Connection not successful, using mock objects")
            self.powerSupplyController = PowerSupplyControllerMock()
            self.electronicLoadController = ElectronicLoadControllerMock()
            self.multimeterController = MultimeterControllerMock()

        # Create an event to indicate if test is running
        self.event = threading.Event()

    # Defining basic functionality of all remote devices through the device controller
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
        x = self.multimeterController.getVolts()
        return float(x)
    def getCurrent(self):
        return (float(self.powerSupplyController.getCurrent()) - float(self.electronicLoadController.getCurrent()))

    def setMaxVoltage(self, volts : float):
        self.powerSupplyController.setMaxVoltage(volts)
    def setMaxVoltageMax(self):
        self.powerSupplyController.setVoltageMax()
    def setMaxCurrent(self, amps : float):
        self.powerSupplyController.setMaxCurrent(amps)
    def setMaxCurrentMax(self):
        self.powerSupplyController.setCurrentMax()
    def setMaxPower(self, watts : float):
        self.powerSupplyController.setMaxPower(watts)
    def setMaxPowerMax(self):
        self.powerSupplyController.setPowerMax()

    # Test protocal for testing the capacity of a battery
    def capacityTest(self, chargeTime : int, waitTime : int, numCycles : int, CPar, temp : int):
        # Clear event to indicate that test is currently running
        self.event.clear()
        # Create a loop that will run one time for each element of the eather CPar or TempPar
        for cParameter in CPar: 
            # Create a list that will keep track of the estemated capacity of the battery
            ampHourCapacity = []
            # Create a loop for each cycle for the cParameter
            for cycleNumber in range(int(numCycles)): 
                # dataStorage object to keep track of tets data
                dataStorage = DataStorage()
                # Variable to keep track of Amp second capacity
                ASeconds = 0
                # Charge with a constant voltage of self.OCVFull
                self.chargeCV(self.OCVFull)
                # Wait the desired amount of minutes
                print(f"Charging for {chargeTime} min")
                for i in range(floor(float(chargeTime) * 60)):
                    # If the test is manualy stopped, break the loop
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
                    # optain and store voltage and current
                    v = self.getVoltage()
                    c = self.getCurrent()
                    dataStorage.addVoltage(v)
                    dataStorage.addCurrent(c)
                    if (float(v) < self.OCVEmpty):
                        break
                    time.sleep(1)
                    ASeconds += self.C_rate * cParameter
                # Stop discharging the battery 
                self.electronicLoadController.stopDischarge()
                # Graph results of current test 
                dataStorage.graphCapacity(cycleNumber, temp, cParameter)
                # Put results of current test in a table
                dataStorage.createTable("Capacity Test", cParameter, cycleNumber, temp )
                print(f"Capacity stored for cycle nr.{cycleNumber + 1} with C-rate of {cParameter}")
                # Store the amp hour capacity for the current test
                ampHourCapacity.append([ASeconds / 3600])
            print(ampHourCapacity)
        # Set the event to indicate that testing is done
        self.event.set()

    def enduranceTest(self, chargeTime : int, waitTime : int, numCycles : int, CPar, temp : int):
        self.event.clear()
        # Create a loop that will run one time for each element of the eather CPar or TempPar
        for cParameter in CPar: 
            # Create a list that will keep track of the estemated capacity of the battery
            ampHourCapacity = []
            # Create a loop for each cycle for the cParameter
            for cycleNumber in range(int(numCycles)): 
                # dataStorage object to keep track of tets data
                dataStorage = DataStorage()
                # Variable to keep track of Amp second capacity
                ASeconds = 0
                # Charge with a constant voltage of self.OCVFull
                self.chargeCV(self.OCVFull)
                # Wait the desired amount of minutes
                print(f"Charging for {chargeTime} min")
                for i in range(floor(float(chargeTime) * 60)):
                    # Break the loop if the testing has been manualy stopped
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
                    # Optain and store voltage and current
                    v = self.getVoltage()
                    c = self.getCurrent()
                    dataStorage.addVoltage(v)
                    dataStorage.addCurrent(c)
                    if (float(v) < self.OCVEmpty):
                        break
                    time.sleep(1)
                    ASeconds += self.C_rate * cParameter
                # Stop discharging battery
                self.electronicLoadController.stopDischarge()
                # Create a table from the current test data
                dataStorage.createTable("Endurance Test", cParameter, cycleNumber, temp )
                
                ampHourCapacity.append([ASeconds / 3600])
            # Create a graph from the current test data
            dataStorage.graphEndurance(temp, cParameter, ampHourCapacity)
            print(ampHourCapacity)
        # Set the event to indicate that testing is finished
        self.event.set()

            

            
class DataStorage:

    def __init__(self) -> None:
        # Empty arrays for data
        self.volts = []
        self.current = []
        self.power = []
        self.amphours = []

    # Function to add voltage value
    def addVoltage(self, votls : float):
        self.volts.append(float('{:.4f}'.format(votls)))

    # Function to add current value
    def addCurrent(self, ampers : float):
        self.current.append(float('{:.4f}'.format(ampers)))

    # Function for creating a table
    def createTable(self, testName : string, c_rate : float, cycleNr : int, temperature : float):
        # Create all the power values by multipling the voltage and current
        for i in range(len(self.volts)):
            self.power.append(self.volts[i] * self.current[i])
        length = len(self.volts)
        # Create a 2 dimensional list for the data
        data = [[]]
        # Fill the list with the results
        for j in range(len(self.volts)):
            d = [j, self.volts[j], self.current[j], self.power[j]]
            data.append(d)
        # Create a table from the 2 dimentional array
        head = ["Time in seconds", "Volts", "Current", "Power"]
        table = tabulate(data, headers=head, tablefmt="simple")
        print(table)  
        # Store the table in a text file
        today = date.today() 
        try:
            with open(f"Desktop/ALOR/Al-ion Battery Test Software/Data/{testName} for {c_rate}C nr. {cycleNr + 1} at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".txt", "w") as f:
                f.write(str(table))
        except:
            with open(os.path.abspath(f"Data/{testName} for {c_rate}C nr. {cycleNr + 1} at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".txt", "w")) as f:
                f.write(str(table))
        # Empty the result values
        self.volts = []
        self.current = []
        self.power = []

    def graphCapacity(self, cyclenumber, temperature, C_rate):
        # Label the graph correctly
        plt.style.use("ggplot")
        plt.xlabel("Time (S)")
        plt.ylabel("Voltage (V)")
        plt.title(f"Capacity at {temperature}° celsius with {C_rate} C current")
        plt.plot(range(len(self.volts)), self.volts, color = "#3a55b4")
        # Calculate the amphour capacity
        ahCapacity = len(self.volts) / 3600
        # Inclue the amphour capacity in the graph
        plt.legend([f"{'{:.2f}'.format(ahCapacity)} aH Capacity"])
        # Store the graph in a file
        try:
            plt.savefig(f"Desktop/ALOR/Al-ion Battery Test Software/Data/Capacity test for {C_rate}C nr. {cyclenumber + 1} at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".png")
        except:
            plt.savefig(os.path.abspath(f"Data/Capacity test for {C_rate}C nr. {cyclenumber + 1} at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".png"))
        # Clear the graph
        plt.clf()
        

    def graphEndurance(self, temperature, C_rate, ampHours):
        # Label the graph correctly
        plt.style.use("ggplot")
        plt.ylabel("Capacity (Ah)")
        plt.xlabel("Cycle number")
        plt.title(f"Change in capacity at {temperature}° celsius with {C_rate} C current")
        plt.plot(range(len(ampHours)), ampHours, "o", color = "#3a55b4")
        # Store the graph in a file
        try:
            plt.savefig(f"Desktop/ALOR/Al-ion Battery Test Software/Data/Endurance test for {C_rate}C at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".png")
        except:
            plt.savefig(os.path.abspath(f"Data/Endurance test for {C_rate}C at {temperature}° celsius     "  + str(datetime.now().strftime("%d_%m_%Y %H_%M_%S")) + ".png"))
        # Clear the graph
        plt.clf()
        


