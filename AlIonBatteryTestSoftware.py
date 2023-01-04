import datetime
from math import floor
import string
import time
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import threading
from AlIonTestSoftwareDeviceDrivers import PowerSupplyController, ElectronicLoadController, MultimeterController
from AlIonTestSoftwareDeviceDriversMock import PowerSupplyControllerMock, ElectronicLoadControllerMock, MultimeterControllerMock
from AlIonTestSoftwareDataManagement import DataStorage
import os
import pandas as pd




# Class used to control test procedures
class TestController:
    # Indicates the number of seconds betwean each measurement
    timeInterval = 0.2

    # Variable for keeping track of the open csircuit voltage of a full battery
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
                dataStorage.createTable("Capacity Test", cParameter, cycleNumber, temp, self.timeInterval, chargeTime )
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
                dataStorage.createTable("Endurance Test", cParameter, cycleNumber, temp, self.timeInterval, chargeTime )
                
                ampHourCapacity.append([ASeconds / 3600])
            # Create a graph from the current test data
            dataStorage.graphEndurance(temp, cParameter, ampHourCapacity)
            print(ampHourCapacity)
        # Set the event to indicate that testing is finished
        self.event.set()




    def upsTest(self, chargeTime : int, dischargeTime : int, waitTime : int, numCycles : int, CPar, temp : int):
        startTime = time.time()
        currentMeasurement = 1.0
        self.event.clear()
        # Create a loop that will run one time for each element of the eather CPar or TempPar
        for cParameter in CPar: 
            # Create a loop for each cycle for the cParameter
            for cycleNumber in range(int(numCycles)): 
                # dataStorage object to keep track of tets data
                dataStorage = DataStorage()
                # Charge with a constant voltage of self.OCVFull
                self.chargeCV(self.OCVFull)
                # Wait the desired amount of minutes
                print(f"Charging for {chargeTime} min")
                for i in range(floor(float(chargeTime) * 60 * (1 / self.timeInterval))):
                    nextMeasurement = startTime + (currentMeasurement - 1) * self.timeInterval - time.time()
                    if(nextMeasurement > 0.0):
                        time.sleep(nextMeasurement)
                    # Break the loop if the testing has been manualy stopped
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    # Optain and store voltage and current
                    v = self.getVoltage()
                    c = self.getCurrent()
                    dataStorage.addVoltage(v)
                    dataStorage.addCurrent(c)
                    currentMeasurement += 1
                # Once the OCV has reached OCVFull we can start discharging
                self.stopCharge()
                # Wait the desired number of seconds
                print(f"Wating for {waitTime} min")
                for i in range(floor(float(waitTime) * 60)):
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    v = self.getVoltage()
                    c = self.getCurrent()
                    dataStorage.addVoltage(v)
                    dataStorage.addCurrent(c)
                    time.sleep(1)
                # Discharging at c rate current
                self.dischargeCC(float(self.C_rate) * float(cParameter))
                # Creating a loop that will break once voltage has reached desired levels
                print(f"Starting discharge in cycle nr.{cycleNumber + 1} with discharge rate {cParameter}C")
                for i in range(floor(float(dischargeTime) * 60.0 * (1 / self.timeInterval))):
                    nextMeasurement = startTime + (currentMeasurement - 1) * self.timeInterval - time.time()
                    if(nextMeasurement > 0.0):
                        time.sleep(nextMeasurement)
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    # Optain and store voltage and current
                    v = self.getVoltage()
                    c = self.getCurrent()
                    dataStorage.addVoltage(v)
                    dataStorage.addCurrent(c)
                    currentMeasurement += 1
                # Stop discharging battery
                self.electronicLoadController.stopDischarge()
                # Create a table from the current test data
                dataStorage.createTable("UPS Test", cParameter, cycleNumber, temp, self.timeInterval, chargeTime)
        # Set the event to indicate that testing is finished
        self.event.set()


    def PhotoVoltaicTest(self, waitTime : int, numCycles : int, CParCharge, CParDischarge, temp : int):
        startTime = time.time()
        currentMeasurement = 1.0
        self.event.clear()
        # Create a loop that will run one time for each element of the eather CPar or TempPar
        for cParameter in CParCharge: 
            # Create a loop for each cycle for the cParameter
            for cycleNumber in range(int(numCycles)): 
                # dataStorage object to keep track of tets data
                dataStorage = DataStorage()
                # Charge with a constant current
                self.chargeCC(float(cParameter) * float(self.C_rate))
                # Wait until the desired voltage is reached
                print(f"Charging")
                chargingStartTime = time.time()
                while (True):
                    nextMeasurement = startTime + (currentMeasurement - 1) * self.timeInterval - time.time()
                    if(nextMeasurement > 0.0):
                        time.sleep(nextMeasurement)
                    if (self.event.is_set()):
                        print("Testing has beed manually stopped")
                        self.event.clear()
                        exit()
                    # Optain and store voltage and current
                    v = self.getVoltage()
                    c = self.getCurrent()
                    dataStorage.addVoltage(v)
                    dataStorage.addCurrent(c)
                    print("Volts: " + str(v) )
                    print("Amps: " + str(c) + "/n")
                    if (float(v) > self.OCVFull or float(time.time() - chargingStartTime > 36000)):
                        break
                # Once the OCV has reached OCVFull we can start discharging
                self.stopCharge()
                # Discharging at c rate current
                self.dischargeCC(float(self.C_rate) * float(CParDischarge))
                # Creating a loop that will break once voltage has reached desired levels
                print(f"Starting discharge in cycle nr.{cycleNumber + 1} with discharge rate {cParameter}C")
                while (True):
                    nextMeasurement = startTime + (currentMeasurement - 1) * self.timeInterval - time.time()
                    if(nextMeasurement > 0.0):
                        time.sleep(nextMeasurement)
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
                # Stop discharging battery
                self.electronicLoadController.stopDischarge()
                # Create a table from the current test data
                dataStorage.createTable("Endurance Test", cParameter, cycleNumber, temp, self.timeInterval )
        # Set the event to indicate that testing is finished
        self.event.set()