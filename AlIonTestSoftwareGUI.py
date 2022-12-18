from math import floor
from sqlite3 import connect
import tkinter
import tkinter.messagebox
import customtkinter
import matplotlib.pyplot as plt
from tkinter import *
import customtkinter
from AlIonBatteryTestSoftware import TestController
from matplotlib.animation import FuncAnimation
import os






customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

counter = 0

counting = FALSE



class GUI(customtkinter.CTk):

    actionButtonColor = "#054279"

    noTestRunningColor = "#48BF91"

    testRunningColor = "#d91e18"
    




    WIDTH = 870
    HEIGHT = 520


    def __init__(self):
        

        self.testController = TestController()


        self.counter = 0

        self.OCVFull = 0.0

        self.OCVEmpty = 0.0

        self.C_rate = 0.0

        self.maxVoltage = 10

        self.maxCurrent = 10

        self.maxPower = 10

        self.testType = ""

        self.volts = []

        self.amps = []

        self.watts = []




        super().__init__()

        

        self.title("ALOR Battery Test Software")
        try:
            self.iconphoto(False, tkinter.PhotoImage(file=os.path.abspath("Desktop\ALOR\Al-ion Battery Test Software\\blackALOR.png")))
        except:
            self.iconphoto(False, tkinter.PhotoImage(file=os.path.abspath("blackALOR.png")))
        self.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when GUI gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_ATS = customtkinter.CTkFrame(master=self)
        self.frame_ATS.grid(row=0, column=1, columnspan = 3, sticky="nswe", padx=20, pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=4, sticky="nswe", padx=20, pady=20)

        # ============ frame_ATS ============

        # configure grid layout (1x11)
        self.frame_ATS.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_ATS.grid_rowconfigure(6, weight=1)  # empty row as spacing
        self.frame_ATS.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_ATS.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_ATS,
                                              text="Automated test sequence",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_change_battery_data = customtkinter.CTkButton(master=self.frame_ATS,
                                                             text="Change battery",
                                                             command=self.changeBatteryValues)
        self.button_change_battery_data.grid(row=10, column=0, pady=10, padx=10, sticky="e")

        self.button_capacityTest = customtkinter.CTkButton(master=self.frame_ATS,
                                                            text="Capacity Test", 
                                                            width=200,
                                                            command=self.capacityTest,
                                                            fg_color=self.actionButtonColor)
        self.button_capacityTest.grid(row=2, column=0, pady=10, padx=10, sticky="n")

        self.button_enduranceTest = customtkinter.CTkButton(master=self.frame_ATS,
                                                            text="Endurance Test", 
                                                            width=200,
                                                            command=self.enduranceTest,
                                                            fg_color=self.actionButtonColor)
        self.button_enduranceTest.grid(row=3, column=0, pady=10, padx=10, sticky="n")

        self.button_upsTest = customtkinter.CTkButton(master=self.frame_ATS,
                                                            text="UPS Test", 
                                                            width=200,
                                                            command=self.upsTest,
                                                            fg_color=self.actionButtonColor)
        self.button_upsTest.grid(row=4, column=0, pady=10, padx=10, sticky="n")

        self.button_photoVoltaicTest = customtkinter.CTkButton(master=self.frame_ATS,
                                                            text="Photovoltaic Test", 
                                                            width=200,
                                                            command=self.photoVoltaicTest,
                                                            fg_color=self.actionButtonColor)
        self.button_photoVoltaicTest.grid(row=5, column=0, pady=10, padx=10, sticky="n")

        self.button_graphLive = customtkinter.CTkButton(master=self.frame_ATS,
                                                        text="Graph live",
                                                        width=200,
                                                        command=self.graphLive)
        self.button_graphLive.grid(row=6, column=0, pady=10, padx=10, sticky="n")

        self.label_runningTest = customtkinter.CTkLabel(master=self.frame_ATS,
                                                        text="No Test is currently running",
                                                        text_font=("Roboto Medium", -16),
                                                        width=200,
                                                        )
        self.label_runningTest.grid(row=8, column=0, pady=10, padx=10, sticky="n")

        self.label_runningTest.configure(bg=self.noTestRunningColor)



        # ============ frame_right ============



        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=1, columnspan=2, rowspan=6, pady=10, padx=10, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(5, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.button_charge = customtkinter.CTkButton(master=self.frame_info,
                                                     text = "Charge",
                                                     command=self.charge,
                                                     width=150,
                                                     fg_color=self.actionButtonColor)
        self.button_charge.grid(row=0, sticky="w", padx=10, pady=10)

        self.button_discharge = customtkinter.CTkButton(master=self.frame_info,
                                                     text = "Discharge",
                                                     command=self.discharge,
                                                     width=150,
                                                     fg_color=self.actionButtonColor)
        self.button_discharge.grid(row=0, sticky="e", padx=10, pady=10)

        # self.radio_var = tkinter.IntVar(value=0)

        self.chargeVar = IntVar()

        self.raidio_button_charge_CV = customtkinter.CTkRadioButton(master=self.frame_info,
                                                                    text="Constant Voltage",
                                                                    variable=self.chargeVar,
                                                                    value = 1)
        self.raidio_button_charge_CV.grid(row=1, pady=10, padx=20, sticky="w")

        
        self.raidio_button_charge_CC = customtkinter.CTkRadioButton(master=self.frame_info,
                                                                    text="Constant Current",
                                                                    variable=self.chargeVar,
                                                                    value = 2)
        self.raidio_button_charge_CC.grid(row=2, pady=10, padx=20, sticky="w")

        self.raidio_button_charge_CP = customtkinter.CTkRadioButton(master=self.frame_info,
                                                                    text="Constant Power",
                                                                    variable=self.chargeVar,
                                                                    value = 3)
        self.raidio_button_charge_CP.grid(row=3, pady=10, padx=20, sticky="w")



        self.dischargeVar = IntVar()

        self.raidio_button_discharge_CV = customtkinter.CTkRadioButton(master=self.frame_info,
                                                                    text="Constant Voltage",
                                                                    variable=self.dischargeVar,
                                                                    value = 1)
        self.raidio_button_discharge_CV.grid(row=1, pady=10, padx=20, sticky="e")

        self.raidio_button_discharge_CC = customtkinter.CTkRadioButton(master=self.frame_info,
                                                                    text="Constant Current",
                                                                    variable=self.dischargeVar,
                                                                    value = 2)
        self.raidio_button_discharge_CC.grid(row=2, pady=10, padx=23, sticky="e")

        self.raidio_button_discharge_CP = customtkinter.CTkRadioButton(master=self.frame_info,
                                                                    text="Constant Power",
                                                                    variable=self.dischargeVar,
                                                                    value = 3)
        self.raidio_button_discharge_CP.grid(row=3, pady=10, padx=29, sticky="e")


        self.entry_charge = customtkinter.CTkEntry(master=self.frame_info)
        self.entry_charge.grid(row=4, pady=10, padx=10, sticky="w")
        
        self.entry_discharge = customtkinter.CTkEntry(master=self.frame_info)
        self.entry_discharge.grid(row=4, pady=10, padx=10, sticky="e")


        self.button_stop = customtkinter.CTkButton(self.frame_info, 
                                                   text="Stop",
                                                   command=self.stop,
                                                   width = 320)

        self.button_stop.grid(row=5, padx=10,pady=10)

 


        # ============ frame_right ============
        self.switchMaxVVar = IntVar()
        self.switch_max_V = customtkinter.CTkSwitch(master=self.frame_right,
                                                variable=self.switchMaxVVar,
                                                command=self.switchMaxVFunc,
                                                text="Max Voltage (V)")
        self.switch_max_V.grid(row=0, column=3, columnspan=1, pady=10, padx=20, sticky="e")

        self.entry_max_V = customtkinter.CTkEntry(master=self.frame_right)
        self.entry_max_V.grid(row=1, column=3, pady=10, padx=20, sticky="e")

        self.switchMaxCVar = IntVar()
        self.switch_max_C = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="Max Current (C)",
                                                variable=self.switchMaxCVar,
                                                command=self.switchMaxCFunc)
        self.switch_max_C.grid(row=2, column=3, columnspan=1, pady=10, padx=20, sticky="e")

        self.entry_max_C = customtkinter.CTkEntry(master=self.frame_right)
        self.entry_max_C.grid(row=3, column=3, pady=10, padx=20, sticky="e")

        self.switchMaxPVar = IntVar()
        self.switch_max_P = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="Max Power (W)",
                                                variable=self.switchMaxPVar,
                                                command=self.switchMaxPFunc)
        self.switch_max_P.grid(row=4, column=3, columnspan=1, pady=10, padx=20, sticky="e")

        self.entry_max_P = customtkinter.CTkEntry(master=self.frame_right)
        self.entry_max_P.grid(row=5, column=3, pady=10, padx=20, sticky="e")

        self.label_V = customtkinter.CTkLabel(master = self.frame_right, text = "0.0 V", text_font=("Roboto Medium", -30))
        self.label_V.grid(row=6, column=1, padx=15,pady=15,sticky="nw")

        self.label_P = customtkinter.CTkLabel(master = self.frame_right, text = "0.0 W", text_font=("Roboto Medium", -30))
        self.label_P.grid(row=6, column=3, padx=15,pady=15, sticky="ne")

        self.label_C = customtkinter.CTkLabel(master = self.frame_right, text = "0.0 A", text_font=("Roboto Medium", -30))
        self.label_C.grid(row=8, column=1, padx=15,pady=15, sticky="sw")

        self.label_T = customtkinter.CTkLabel(master = self.frame_right, text ="0.0 S", text_font=("Roboto Medium", -30))
        self.label_T.grid(row=8, column=3, padx=15,pady=15, sticky="se")

        self.button_start_timer = customtkinter.CTkButton(master = self.frame_right, text = "Start timer", command = self.startTimer)
        self.button_start_timer.grid(row=6,column=2,padx=10,pady=5)

        self.button_stop_timer = customtkinter.CTkButton(master = self.frame_right, text = "Stop timer", command = self.stopTimer)
        self.button_stop_timer.grid(row=7,column=2,padx=10,pady=5)

        self.button_reset_timer = customtkinter.CTkButton(master = self.frame_right, text = "Reset timer", command = self.resetTimer)
        self.button_reset_timer.grid(row=8,column=2,padx=10,pady=5)


        self.changeBatteryValues()

        self.button_cancel_battery.configure(state="disabled")

        self.timeloop()


    def timeloop(self):
        try:
            global counter
            global counting
            if counting == TRUE:
                counter += 1
                if (counter < 60):
                    self.label_T.configure(text = str(counter) + " S")
                elif (counter < 3600):
                    self.label_T.configure(text = str(floor(counter / 60)) + " M " + str(counter % 60) + " S")
                else:
                    self.label_T.configure(text = str(floor(counter / 3600)) + "H" + str(floor((counter % 3600) / 60)) + " M " + str(counter % 60) + " S")
            
            volts = self.testController.getVoltage()
            current = self.testController.getCurrent()
            self.label_V.configure(text= '{:06.2f}'.format(volts) + " V")
            self.label_C.configure(text= '{:06.2f}'.format(current) + " A")
            self.label_P.configure(text= '{:06.2f}'.format(float(volts) * float(current)) + " W")
            self.volts.append(float(volts))
            self.amps.append(float(current))
            self.watts.append(float(volts) * float(current))

            if (self.testController.event.is_set()):
                if (self.testType != ""):
                    self.enableOperations()
                    self.label_runningTest.configure(bg = self.noTestRunningColor)
                    self.label_runningTest.configure(text="No test is currently running")
                    self.testType = ""
        except:
            self.quit()
        



        


        try:
            (self.batteryValuesWindow.state())
            try:
                float(self.entryOCVFullTextVar.get())
                float(self.entryOCVEmptyTextVar.get())
                float(self.entryCRateTextVar.get())
                self.button_save_battery.configure(state = "enabled")
            except:
                self.button_save_battery.configure(state = "disabled")

        except:
            pass
        self.button_change_battery_data.after(1000, self.timeloop)


    def capacityTest(self):
        self.testType = "capacity test"
        self.startAutomatedTestSequence()

    def enduranceTest(self):
        self.testType = "endurance test"
        self.startAutomatedTestSequence()

    def upsTest(self):
        self.testType = "ups test"
        self.startAutomatedTestSequence()

    def photoVoltaicTest(self):
        self.testType = "photovoltaic test"
        self.startAutomatedTestSequence()

    def graphLive(self):
        plt.style.use("ggplot")
        self.fig, ax = plt.subplots()
        self.animationVolts = FuncAnimation(self.fig, self.funcAnimateVolts, interval = 30000)
        plt.xlabel("Time (S)")
        plt.ylabel("Volts (Blátt)    Amps (Gult)    Watts (Rautt) ")

        plt.show()
    
    def funcAnimateVolts(self, i):
        try:
            self.fig = plt.plot(self.volts, color=self.actionButtonColor)
            self.fig = plt.plot(self.amps, color="r")
            self.fig= plt.plot(self.watts, color="y")
        except:
            self.animationVolts.pause()




    def switchMaxVFunc(self):
        if (self.switchMaxVVar.get() == 1): 
            try:
                float(self.entry_max_V.get())
                self.entry_max_V.configure(state="disabled")
                self.maxPower = float(self.entry_max_V.get())
                
                self.testController.setMaxVoltage(float(self.entry_max_V.get()))
                    
            except ValueError:
                self.switch_max_V.deselect()
        else:
            self.entry_max_V.configure(state="normal")
            self.maxVoltage = 100
                
            self.testController.setMaxVoltageMax()



    def switchMaxCFunc(self):
        if (self.switchMaxCVar.get() == 1): 
            try:
                float(self.entry_max_C.get())
                self.entry_max_C.configure(state="disabled")
                self.maxCurrent = float(self.entry_max_C.get())

                self.testController.setMaxCurrent(float(self.entry_max_C.get()))
            except ValueError:
                self.switch_max_C.deselect()
        else:
            self.entry_max_C.configure(state="normal")
            self.maxCurrent = 100

            self.testController.setMaxCurrentMax()


    def switchMaxPFunc(self):
        if (self.switchMaxPVar.get() == 1): 
            try:
                float(self.entry_max_P.get())
                self.entry_max_P.configure(state="disabled")
                self.maxPower = float(self.entry_max_P.get())
                
                self.testController.setMaxPower(float(self.entry_max_P.get()))
            except ValueError:
                self.switch_max_P.deselect()
        else:
            self.entry_max_P.configure(state="normal")
            self.maxPower = 100
            if (connect):
                self.testController.setMaxPowerMax()



    def startAutomatedTestSequence(self):
        
        self.disableOperations()


        self.automatetTestSequenceWindow = customtkinter.CTkToplevel()

        self.automatetTestSequenceWindow.title("Testing information")

        try:
            self.automatetTestSequenceWindow.iconphoto(False, tkinter.PhotoImage(file=os.path.abspath("Desktop\ALOR\Al-ion Battery Test Software\\blackALOR.png")))
        except:
            self.automatetTestSequenceWindow.iconphoto(False, tkinter.PhotoImage(file=os.path.abspath("blackALOR.png")))
        self.label_ChargeTime = customtkinter.CTkLabel(master=self.automatetTestSequenceWindow,
                                               text = "Charging time (minutes):")
        self.label_ChargeTime.grid(row=0,column=1,padx=10,pady=10, sticky = "w")
        
        self.entryChargeTimeTextVar = StringVar()
        self.entryChargeTime = customtkinter.CTkEntry(master=self.automatetTestSequenceWindow, textvariable=self.entryChargeTimeTextVar)
        self.entryChargeTime.grid(row=0,column=2,padx=10,pady=10, sticky = "w")
        self.entryChargeTimeTextVar.set(0)


        self.label_DischargeTime = customtkinter.CTkLabel(master=self.automatetTestSequenceWindow,
                                               text = "Discharging time (minutes):")
        self.label_DischargeTime.grid(row=1,column=1,padx=10,pady=10, sticky = "w")

        self.entryDischargeTimeTextVar = StringVar()
        self.entryDischargeTime = customtkinter.CTkEntry(master=self.automatetTestSequenceWindow, textvariable=self.entryDischargeTimeTextVar)
        self.entryDischargeTime.grid(row=1,column=2,padx=10,pady=10, sticky = "w")
        self.entryDischargeTimeTextVar.set(0)


        self.label_WaitTime = customtkinter.CTkLabel(master=self.automatetTestSequenceWindow,
                                               text = "Waiting time (minutes):")
        self.label_WaitTime.grid(row=2,column=1,padx=10,pady=10, sticky = "w")

        self.entryWaitTimeTextVar = StringVar()
        self.entryWaitTime = customtkinter.CTkEntry(master=self.automatetTestSequenceWindow, textvariable=self.entryWaitTimeTextVar)
        self.entryWaitTime.grid(row=2,column=2,padx=10,pady=10, sticky = "w")
        self.entryWaitTimeTextVar.set(0)


        self.label_numCycles = customtkinter.CTkLabel(master=self.automatetTestSequenceWindow,
                                               text = "Number of cycles:")
        self.label_numCycles.grid(row=3,column=1,padx=10,pady=10, sticky = "w")

        self.entryNumCyclesTextVar = StringVar()
        self.entryNumCycles = customtkinter.CTkEntry(master=self.automatetTestSequenceWindow, textvariable=self.entryNumCyclesTextVar)
        self.entryNumCycles.grid(row=3,column=2,padx=10,pady=10, sticky = "w")
        self.entryNumCyclesTextVar.set(0)


        self.label_cParCharge = customtkinter.CTkLabel(master=self.automatetTestSequenceWindow,
                                               text = "C-rate Charging Parameters:")
        self.label_cParCharge.grid(row=4,column=1,padx=10,pady=10, sticky = "w")

        self.entryCParChargeTextVar = StringVar()
        self.entryCParCharge = customtkinter.CTkEntry(master=self.automatetTestSequenceWindow, textvariable=self.entryCParChargeTextVar)
        self.entryCParCharge.grid(row=4,column=2,padx=10,pady=10, sticky = "w")
        self.entryCParChargeTextVar.set(0)

        self.label_cParDischarge = customtkinter.CTkLabel(master=self.automatetTestSequenceWindow,
                                               text = "C-rate Discharging Parameters:")
        self.label_cParDischarge.grid(row=5,column=1,padx=10,pady=10, sticky = "w")

        self.entryCParDischargeTextVar = StringVar()
        self.entryCParDischarge = customtkinter.CTkEntry(master=self.automatetTestSequenceWindow, textvariable=self.entryCParDischargeTextVar)
        self.entryCParDischarge.grid(row=5,column=2,padx=10,pady=10, sticky = "w")
        self.entryCParDischargeTextVar.set(0)

        self.label_TempPar = customtkinter.CTkLabel(master=self.automatetTestSequenceWindow,
                                               text = "Temperature (celsius):")
        self.label_TempPar.grid(row=6,column=1,padx=10,pady=10, sticky = "w")

        self.entryTempParTextVar = StringVar()
        self.entryTempPar = customtkinter.CTkEntry(master=self.automatetTestSequenceWindow, textvariable=self.entryTempParTextVar)
        self.entryTempPar.grid(row=6,column=2,padx=10,pady=10, sticky = "w")
        self.entryTempParTextVar.set(0)



        self.button_run_test = customtkinter.CTkButton(master = self.automatetTestSequenceWindow, text="Run", command=self.runTest, fg_color=self.actionButtonColor)
        self.button_run_test.grid(row=7,column=2,padx=10, pady=10)

        self.button_cancel_test = customtkinter.CTkButton(master = self.automatetTestSequenceWindow, text="Cancel", command=self.cancelTest)
        self.button_cancel_test.grid(row=7,column=1,padx=10, pady=10)


        

    def changeBatteryValues(self):
        
        self.disableOperations()


        self.batteryValuesWindow = customtkinter.CTkToplevel()

        self.batteryValuesWindow.title("Battery information")

        try:
            self.batteryValuesWindow.iconphoto(False, tkinter.PhotoImage(file=os.path.abspath("Desktop\ALOR\Al-ion Battery Test Software\\blackALOR.png")))
        except:
            self.batteryValuesWindow.iconphoto(False, tkinter.PhotoImage(file=os.path.abspath("blackALOR.png")))

        self.label_OCVFull = customtkinter.CTkLabel(master=self.batteryValuesWindow,
                                               text = "Upper limit voltage (V):")
        self.label_OCVFull.grid(row=0,column=1,padx=10,pady=10, sticky = "w")

        self.label_OCVEmpty = customtkinter.CTkLabel(master=self.batteryValuesWindow,
                                               text = "Lower limit voltage (V):")
        self.label_OCVEmpty.grid(row=1,column=1,padx=10,pady=10, sticky = "w")

        self.label_CRate = customtkinter.CTkLabel(master=self.batteryValuesWindow,
                                               text = "C-rate (A):")
        self.label_CRate.grid(row=2,column=1,padx=10,pady=10, sticky = "w")

        self.entryOCVFullTextVar = StringVar()
        self.entry_OCVFull = customtkinter.CTkEntry(master=self.batteryValuesWindow, textvariable=self.entryOCVFullTextVar)
        self.entry_OCVFull.grid(row=0,column=2,padx=10,pady=10, sticky = "w")
        self.entryOCVFullTextVar.set(self.OCVFull)

        self.entryOCVEmptyTextVar = StringVar()
        self.entry_OCVEmpty = customtkinter.CTkEntry(master=self.batteryValuesWindow, textvariable=self.entryOCVEmptyTextVar)
        self.entry_OCVEmpty.grid(row=1,column=2,padx=10,pady=10, sticky = "w")
        self.entryOCVEmptyTextVar.set(self.OCVEmpty)

        self.entryCRateTextVar = StringVar()
        self.entry_CRate = customtkinter.CTkEntry(master=self.batteryValuesWindow, textvariable=self.entryCRateTextVar)
        self.entry_CRate.grid(row=2,column=2,padx=10,pady=10, sticky = "w")
        self.entryCRateTextVar.set(self.C_rate)



        self.button_save_battery = customtkinter.CTkButton(master = self.batteryValuesWindow, text="Save", command=self.saveBattery)
        self.button_save_battery.grid(row=5,column=2,padx=10, pady=10)

        self.button_cancel_battery = customtkinter.CTkButton(master = self.batteryValuesWindow, text="Cancel", command=self.cancelBattery)
        self.button_cancel_battery.grid(row=5,column=1,padx=10, pady=10)


    def saveBattery(self):
        
        self.testController.OCVFull = float(self.entryOCVFullTextVar.get())
        self.testController.OCVEmpty = float(self.entryOCVEmptyTextVar.get())
        self.testController.C_rate = float(self.entryCRateTextVar.get())
        self.batteryValuesWindow.destroy()
        self.enableOperations()

    def cancelBattery(self):
        self.batteryValuesWindow.destroy()
        self.enableOperations()

    

    def runTest(self):
        import threading
        if (self.testType == "capacity test"):
            self.testController.event.clear()
            self.capacityThread = threading.Thread(target=self.testController.capacityTest, args=(
                self.entryChargeTimeTextVar.get(),
                self.entryWaitTimeTextVar.get(),
                self.entryNumCyclesTextVar.get(),
                eval("list({" + self.entryCParChargeTextVar.get() + "})" ),
                self.entryTempPar.get()
            ))
            self.capacityThread.start()
        elif (self.testType == "endurance test"):
            self.testController.event.clear()
            self.enduranceThread = threading.Thread(target=self.testController.enduranceTest, args=(
                self.entryChargeTimeTextVar.get(),
                self.entryWaitTimeTextVar.get(),
                self.entryNumCyclesTextVar.get(),
                eval("list({" + self.entryCParChargeTextVar.get() + "})" ),
                self.entryTempParTextVar.get()
            ))
            self.enduranceThread.start()
        elif (self.testType == "ups test"):
            self.testController.event.clear()
            self.upsThread = threading.Thread(target=self.testController.upsTest, args=(
                self.entryChargeTimeTextVar.get(),
                self.entryDischargeTimeTextVar.get(),
                self.entryWaitTimeTextVar.get(),
                self.entryNumCyclesTextVar.get(),
                eval("list({" + self.entryCParChargeTextVar.get() + "})" ),
                self.entryTempParTextVar.get()
            ))
            self.upsThread.start()
        elif (self.testType == "photovoltaic test"):
            self.testController.event.clear()
            self.photovoltaicThread = threading.Thread(target=self.testController.PhotoVoltaicTest, args=(
                self.entryWaitTimeTextVar.get(),
                self.entryNumCyclesTextVar.get(),
                eval("list({" + self.entryCParChargeTextVar.get() + "})" ),
                self.entryCParDischargeTextVar.get(),
                self.entryTempParTextVar.get()
            ))
            self.photovoltaicThread.start()
        self.automatetTestSequenceWindow.destroy()
        self.label_runningTest.configure(bg = self.testRunningColor)
        self.label_runningTest.configure(text = f"Running {self.testType}")

    def cancelTest(self):
        self.automatetTestSequenceWindow.destroy()
        self.enableOperations()





    def charge(self):   
        try:
            float(self.entry_charge.get())
            if (self.entry_charge.get() != ""):
                if (self.chargeVar.get() == 1):
                    self.disableOperations()

                    self.label_runningTest.configure(bg = self.testRunningColor)
                    self.label_runningTest.configure(text = f"Charging constant voltage")
                    self.testController.chargeCV(float(self.entry_charge.get()))
                    
                elif (self.chargeVar.get() == 2):
                    self.disableOperations()

                    self.label_runningTest.configure(bg = self.testRunningColor)
                    self.label_runningTest.configure(text = f"Charging constant current")
                    self.testController.chargeCC(float(self.entry_charge.get()))
                    
                elif (self.chargeVar.get() == 3):
                    self.disableOperations()

                    self.label_runningTest.configure(bg = self.testRunningColor)
                    self.label_runningTest.configure(text = f"Charging constant power")
                    self.testController.chargeCP(float(self.entry_charge.get()))
        except:
            pass


    def discharge(self):
        try:
            float(self.entry_discharge.get())
            if (self.entry_discharge.get() != ""):
                if (self.dischargeVar.get() == 1):
                    self.disableOperations()

                    self.label_runningTest.configure(bg = self.testRunningColor)
                    self.label_runningTest.configure(text = f"Discharging constant voltage")
                    self.testController.dischargeCV(float(self.entry_discharge.get()))
                    
                elif (self.dischargeVar.get() == 2):
                    self.disableOperations()

                    self.label_runningTest.configure(bg = self.testRunningColor)
                    self.label_runningTest.configure(text = f"Discharging constant current")
                    self.testController.dischargeCC(float(self.entry_discharge.get()))
                    
                elif (self.dischargeVar.get() == 3):
                    self.disableOperations()

                    self.label_runningTest.configure(bg = self.testRunningColor)
                    self.label_runningTest.configure(text = f"Discharging constant power")
                    self.testController.dischargeCP(float(self.entry_discharge.get()))
                    
        except:
            pass

    def stop(self):
        self.testController.stopCharge()
        self.testController.stopDischarge()
        self.testController.event.set()
        self.label_runningTest.configure(text="No test is currently running", bg = self.noTestRunningColor)
    
            
        self.enableOperations()

    def startTimer(self):
        global first
        global counting
        counting = TRUE
        
    def stopTimer(self):
        global counting
        counting = FALSE

    def resetTimer(self):
        global counter
        counter = 0
        self.label_T.configure(text="0 S")
    

    def disableOperations(self):

        self.button_change_battery_data.configure(state = "disabled")
        self.button_charge.configure(state = "disabled")
        self.button_discharge.configure(state = "disabled")

        self.button_capacityTest.configure(state = "disabled")
        self.button_enduranceTest.configure(state = "disabled")

        self.button_change_battery_data.configure(state = "disabled")

        self.raidio_button_charge_CV.configure(state = "disabled")
        self.raidio_button_charge_CC.configure(state = "disabled")
        self.raidio_button_discharge_CV.configure(state = "disabled")
        self.raidio_button_discharge_CC.configure(state = "disabled")
        self.raidio_button_discharge_CP.configure(state = "disabled")



        self.switch_max_V.configure(state="disabled")
        self.switch_max_C.configure(state="disabled")
        self.switch_max_P.configure(state="disabled")



    def enableOperations(self):


        self.button_change_battery_data.configure(state = "enabled")
        self.button_charge.configure(state = "enabled")
        self.button_discharge.configure(state = "enabled")

        self.button_capacityTest.configure(state = "enabled")
        self.button_enduranceTest.configure(state = "enabled")

        self.button_change_battery_data.configure(state = "enabled")

        self.raidio_button_charge_CV.configure(state = "normal")
        self.raidio_button_charge_CC.configure(state = "normal")
        self.raidio_button_discharge_CV.configure(state = "normal")
        self.raidio_button_discharge_CC.configure(state = "normal")
        self.raidio_button_discharge_CP.configure(state = "normal")

        self.switch_max_V.configure(state="enabled")
        self.switch_max_C.configure(state="enabled")
        self.switch_max_P.configure(state="enabled")

            

    



    def on_closing(self, event=0):
        self.stop()
        self.destroy()


if __name__ == "__main__":
    gui = GUI()
    gui.batteryValuesWindow.attributes('-topmost', True)

    gui.update()

    gui.mainloop()

#print(os.path.abspath("Desktop\ALOR\Al-ion Battery Test Software\blackALOR.png"))
