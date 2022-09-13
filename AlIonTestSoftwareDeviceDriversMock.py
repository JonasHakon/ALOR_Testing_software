from random import randrange
from tkinter import *


# Class for communication with the NI-VISA driver to control the power supply
class PowerSupplyControllerMock:
    # Variable to keep the resource name of the power supply
    powerSupplyName = "USB0::0x1698::0x0837::011000000136::INSTR"

    maxVoltage = 10
    maxCurrent = 10
    maxPower = 10

    # Function that returns the name of connected device
    def checkDeviceConnection(self):
        print("Mock object is connected")

    # Functions that allow user to set the maximum voltage, current and power for safety
    def setMaxVoltage(self, volts : int):
        self.maxVoltage = volts

    def setMaxCurrent(self, amps : int):
        self.maxCurrent = amps

    def setMaxPower(self, watts : int):
        self.maxPower = watts

    def getVoltage(self):
        return randrange(self.maxVoltage * 10000000) / 100000000

    def getCurrent(self):
        return randrange(self.maxVoltage * 10000000) / 100000000

    def getPower(self):
        return randrange(self.maxVoltage * 10000000) / 100000000
        

    # Function for constant current charging, taking in current in ampers
    def chargeCC (self, ampers : int):
        pass

    # Function for constant voltage charging, taking in voltage in volts
    def chargeCV(self, volts : int):
        pass

    # Function for constant voltage charging, taking in voltage in volts
    def chargeCV(self, watts : int):
        pass

    def stopCharge(self):
        pass

    
    





# Class for communication with the NI-VISA driver to control the electronic load
class ElectronicLoadControllerMock:
    # Variable to keep the resource name of the electronic load
    electronicLoadName = "USB0::0x0A69::0x083E::000000000001::INSTR"

    maxVoltage = 10
    maxCurrent = 10
    maxPower = 10

    # Function that returns the name of the connected device
    def checkDeviceConnection(self):
        print("Mock object is connected")

    def setMaxCurrent(self, amps):
        self.maxCurrent = amps

    def getVolts(self):
        return randrange(self.maxVoltage * 10000000) / 10000000

    def getCurrent(self):
        return randrange(self.maxCurrent * 10000000) / 10000000

    def getPower(self):
        return randrange(self.maxPower * 10000000) / 10000000


    

    def dischargeCV(self, volts):
        pass

    def dischargeCC(self, amps):
        pass

    def dischargeCP(self, watts):
        pass

    def stopDischarge(self):
        pass




# Class for communication with the NI-VISA driver to control the multimeter
class MultimeterControllerMock:
    
    # Variable to keep the resource name of the mutimeter
    multimeterName = "USB0::0x1698::0x083F::TW00014586::INSTR"

    # Function that returns the name of the connected device
    def checkDeviceConnection(self):
        print("Mock object is connected")


    def getTemperature(self):
        return randrange(10000000) / 10000000

    def getVolts(self):
        return randrange(10000000) / 10000000

    def getResistance(self):
        return randrange(10000000) / 10000000


        
