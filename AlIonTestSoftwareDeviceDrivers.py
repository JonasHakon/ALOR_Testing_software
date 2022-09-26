import pyvisa
from tkinter import *


# Class for communication with the NI-VISA driver to control the power supply
class PowerSupplyController:
    # Variable to keep the resource name of the power supply
    powerSupplyName = "USB0::0x1698::0x0837::011000000136::INSTR"

    # Constructor that establishes connection to the power supply
    def __init__(self) -> None:
        self.resourceManager = pyvisa.ResourceManager()
        self.powerSupply = self.resourceManager.open_resource(self.powerSupplyName)
        

    # Function that returns the name of connected device
    def checkDeviceConnection(self):
        print(self.powerSupply.query("*IDN?"))

    # Functions that allow user to set the maximum voltage, current and power for safety
    def setMaxVoltage(self, *volts):
        try:
            self.powerSupply.write("SOUR:VOLT:LIMIT:HIGH " + str((volts[0])))
        except:
            self.powerSupply.write("SOUR:VOLT:LIMIT:HIGH MAX")

    def setMaxCurrent(self, *amps):
        try:
            self.powerSupply.write("SOUR:CURR:LIMIT:HIGH " + str(amps[0]))
        except:
            self.powerSupply.write("SOUR:CURR:LIMIT:HIGH MAX")

    def setMaxPower(self, *watt):
        try:
            self.powerSupply.write("SOUR:POW:PROT:HIGH " + str(watt[0]))
        except:
            self.powerSupply.write("SOUR:POW:PROT:HIGH MAX")

    # Functions to obtain the voltage, current and power from the power supply
    def getVoltage(self):
        return self.powerSupply.query("FETCH:VOLT?")

    def getCurrent(self):
        return self.powerSupply.query("FETCH:CURR?")

    def getPower(self):
        return self.powerSupply.query("FETCH:POW?")
        

    # Function for constant current charging, taking in current in ampers
    def chargeCC (self, ampers : int):
        # Turn of all output
        self.powerSupply.write("CONF:OUTP OFF")
        # Set the voltage amount to max
        self.powerSupply.write("SOUR:VOLT MAX")
        # Set desired current
        self.powerSupply.write("SOUR:CURR " + str(ampers))
        # Turn on output
        self.powerSupply.write("CONF:OUTP ON")

    # Function for constant voltage charging, taking in voltage in volts
    def chargeCV(self, volts : int):
        # Turn of all output
        self.powerSupply.write("CONF:OUTP OFF")
        # Set desired voltiage
        self.powerSupply.write("SOUR:VOLT " + str(volts))
        # Turn on output
        self.powerSupply.write("CONF:OUTP ON")

    # Function for constant voltage charging, taking in voltage in volts
    def chargeCV(self, watts : int):
        # Turn of all output
        self.powerSupply.write("CONF:OUTP OFF")
        # Set desired voltiage
        self.powerSupply.write("PROG:CP:POW " + str(watts))
        # Turn on output
        self.powerSupply.write("CONF:OUTP ON")



    # Functions to stop the powersupply from charging
    def stopCharge(self):
        self.powerSupply.write("CONF:OUTP OFF")

    
    





# Class for communication with the NI-VISA driver to control the electronic load
class ElectronicLoadController:
    # Variable to keep the resource name of the electronic load
    electronicLoadName = "USB0::0x0A69::0x083E::000000000001::INSTR"

    # Constructor that establishes connection to the electronic load
    def __init__(self) -> None:
        self.resourceManager = pyvisa.ResourceManager()
        self.electronicLoad = self.resourceManager.open_resource(self.electronicLoadName)

        # Set and activate the channel that will be used for testing
        self.electronicLoad.write("CHAN 1")
        self.electronicLoad.write("CHAN:ACT 1")

    # Function that returns the name of the connected device
    def checkDeviceConnection(self):
        print(self.electronicLoad.query("*IDN?"))

    # Function that sets the maximum current for the electronic load
    def setMaxCurrent(self, amps):
        self.electronicLoad.write("VOLT:STAT:ILIM " + str(amps))

    # Function that receves a voltage reading from the electronic load
    def getVolts(self):
        return self.electronicLoad.query("FETCH:VOLT?")

    # Function that receves a current reading from the electrinic load
    def getCurrent(self):
        return self.electronicLoad.query("FETCH:CURR?")

    # Function that receves a power reading from the electronic load
    def getPower(self):
        return self.electronicLoad.query("FETCH:POW?")


    

    def dischargeCV(self, volts):
        # Turn output off
        self.electronicLoad.write("LOAD:STAT:OFF")
        # Switch to CV mode
        self.electronicLoad.write("MODE CVH")
        # Set the constant voltage
        self.electronicLoad.write("VOLT:STAT:L1 " + str(volts))
        # Turn on output for connected channel
        self.electronicLoad.write("LOAD:STAT ON")

    def dischargeCC(self, amps):
        # Turn output off
        self.electronicLoad.write("LOAD:STAT:OFF")
        # Switch to CV mode
        self.electronicLoad.write("MODE CCH")
        # Set the desired current
        self.electronicLoad.write("CURR:STAT:L1 " + str(amps))
        # Turn on the output
        self.electronicLoad.write("LOAD:STAT ON")

    def dischargeCP(self, watts):
        # Turn output off
        self.electronicLoad.write("LOAD:STAT:OFF")
        # Switch to CP mode
        self.electronicLoad.write("MODE CPH")
        # Set the desired power
        self.electronicLoad.write("POW:STAT:L1 " + str(watts))
        # Turn output on
        self.electronicLoad.write("LOAD:STAT ON")

    # Function to stop the electronic load from discharging the battery
    def stopDischarge(self):
        self.electronicLoad.write("LOAD:STAT OFF")




# Class for communication with the NI-VISA driver to control the multimeter
class MultimeterController:
    
    # Variable to keep the resource name of the mutimeter
    multimeterName = "USB0::0x1698::0x083F::TW00014586::INSTR"

    # Constructor that establishes connection to the mutimeter
    def __init__(self) -> None:
        self.resourceManager = pyvisa.ResourceManager()
        self.multimeter = self.resourceManager.open_resource(self.multimeterName)

    # Function that returns the name of the connected device
    def checkDeviceConnection(self):
        print(self.multimeter.query("*IDN?"))

    # Function that returns the temperature from the multimeter
    def getTemperature(self):
        return self.multimeter.query("MEAS:TEMP?")

    # Function that returns the voltage from the multimeter
    def getVolts(self):
        return self.multimeter.query("MEAS:VOLT:DC?")

    # Function that returns the resistance from the multimeter
    def getResistance(self):
        return self.multimeter.query("MEAS:RES?")


        