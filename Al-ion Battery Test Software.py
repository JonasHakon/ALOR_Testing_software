from cgi import test
import graphlib
from logging.config import valid_ident
from optparse import Values
import time
from tkinter import Y
import pyvisa
import matplotlib.pyplot as plt





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
    def setMaxVoltage(self, volts : int):
        self.powerSupply.write("SOUR:VOLT:LIMIT:HIGH " + str(volts))

    def setMaxCurrent(self, amps : int):
        self.powerSupply.write("SOUR:CURR:LIMIT:HIGH " + str(amps))

    def setMaxPower(self, watt : int):
        self.powerSupply.write("SOUR:POW:PROT:HIGH " + str(watt))
        

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

    # TODO FIX THE CP FUNCTION AND TEST FOR CORRECT VALUES

    # Function for constant power charging, taking in power in milliamperhours and duration in seconds
    #   def chargeCP (self, milliamphours, seconds):
        # Turn of all output
        #   self.powerSupply.write("CONF:OUTP OFF")
        # Set desired voltiage
        #   self.powerSupply.write("SOUR:POW " + str(milliamphours * 0.001))
        # Turn on output
        #   self.powerSupply.write("CONF:OUTP ON")
    
    # Funtion to stop current charging method
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

    

    def dischargeCV(self, volts):
        # Turn output off
        self.electronicLoad.write("LOAD:STAT:OFF")
        # Set the constant voltage
        self.electronicLoad.write("VOLT:STAT:L1 " + str(volts))
        # Turn on output for connected channel
        self.electronicLoad.write("LOAD:STAT ON")

    def dischargeCC(self, amps):
        # Turn output off
        self.electronicLoad.write("LOAD:STAT:OFF")
        # Set the desired current
        self.electronicLoad.write("CURR:STAT:L1 " + str(amps))
        # Turn on the output
        self.electronicLoad.write("LOAD:STAT ON")

    def dischargeCP(self, watts):
        # Turn output off
        self.electronicLoad.write("LOAD:STAT:OFF")
        # Set the desired power
        self.electronicLoad.write("POW:STAT:L1 " + str(watts))
        # Turn output on
        self.electronicLoad.write("LOAD:STAT ON")

    def stopDischarge(self):
        self.electronicLoad.write("LOAD:STAT OFF")




# Class for communication with the NI-VISA driver to control the multimeter
class multimeterController:
    
    # Variable to keep the resource name of the mutimeter
    multimeterName = "USB0::0x1698::0x083F::TW00014586::INSTR"

    # Constructor that establishes connection to the mutimeter
    def __init__(self) -> None:
        self.resourceManager = pyvisa.ResourceManager()
        self.multimeter = self.resourceManager.open_resource(self.multimeterName)

    # Function that returns the name of the connected device
    def checkDeviceConnection(self):
        print(self.multimeter.query("*IDN?"))


    def getTemp(self):
        return self.multimeter.query("MEAS:TEMP?")

    def getMilliAmps(self):
        return self.multimeter.query("MEAS:CURR:DC?")

    def getVolts(self):
        return self.multimeter.query("MEAS:VOLT:DC?")

    def getResistance(self):
        return self.multimeter.query("MEAS:RES?")
        

class TestController:

    def __init__(self) -> None:
        # self.powerSupplyController = PowerSupplyController()
        self.electronicLoadController = ElectronicLoadController()
        # self.multimeterController = multimeterController()
    
    # Function for capacity testing that takes in the open circuit Voltage of a full battery (OCVFull), the open circuit voltage
    #  of an empty battery (OCVEmpty) and the estemated discharge current for empting the battery in one hour (C)
    def cpacityTest(self, OCVFull : int, OCVEmpty : int, C : int):
        # Charge the battery with constant voltage of OCVFull
        self.powerSupplyController.chargeCV(OCVFull)
        # Stop chargin the battery when the current is below a threshold
        # TODO find an aproprite current threshol
        while (self.multimeterController.getMilliAmps() < "Insert threshhold"):
            time.sleep(1)
        # When battery is full, stop charging
        self.powerSupplyController.stopCharge() 

        # Start discharging with a constant current of C
        self.electronicLoadController.dischargeCC(C)

        # Continue discharging while the voltage of the battery remains above the OCVEmpty
        while(self.multimeterController.getVolts > OCVEmpty):
            time.sleep(1)
        
        # Stop discharging when the Voltage has reached OCV
        self.electronicLoadController.stopDischarge()


    def basicChargeTest(self):
        graph = Graph()
        self.electronicLoadController
        self.electronicLoadController.dischargeCV(1.45)

        time.sleep(30)

        for i in range(600):
            x = self.electronicLoadController.electronicLoad.query("FETCH:CURR?")
             # y = float(x[:-5]) * (10 ** int(x[9:]))
            print(x)
            graph.addValue(x)
            time.sleep(1)
        
        self.electronicLoadController.stopDischarge()

        graph.graphBasicCapacity()




class Graph:
    
    # List to store values
    values = []

    # Function to reset value list
    def clearValues(self):
        self.values = []

    # Function to add values to list
    def addValue(self, value):
        self.values.append(float(value))

    # Function to graph a capacity test
    def graphBasicCapacity(self):
        plt.style.use("ggplot")
        x = list(range(len(self.values)))
        plt.plot(x, self.values)
        plt.xlabel("Time in seconds")
        plt.ylabel("Current")
        plt.title("Battery discharge curve")

        plt.show()


testController = TestController()

testController.basicChargeTest()
