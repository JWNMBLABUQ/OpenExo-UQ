from tkinter import StringVar
from datetime import datetime

class ExoData:
    def __init__(self):
        self.tStep = []
        self.rTorque = []
        self.epochTime = []  # New list to store epoch timestamps
        self.rSetP = []
        self.rState = []
        self.lTorque = []
        self.lSetP = []
        self.lState = []
        self.lFsr = []
        self.rFsr = []
        #added but do we want to keep
        self.rHeelFsr = []
        self.lHeelFsr = []
        self.rAnkleAngle = []
        self.lAnkleAngle = []
        #record our features
        self.MinShankVel = []
        self.MaxShankVel = []
        self.MinShankAng = []
        self.MaxShankAng = []
        self.MaxFSR = []
        self.StanceTime = []
        self.SwingTime = []
        #and the predicted task/state
        self.Task=[]
        self.BatteryPercent=StringVar()
        self.BatteryPercent.set("Battery Voltage: ?")
        self.battery_is_low = False  # Flag to track if battery is low
        self.Mark=[] #mark our Trials
        self.MarkVal=0
        self.MarkLabel=StringVar()
        self.MarkLabel.set("Mark: " +str(self.MarkVal))

    def resetMark(self):
        """Reset the mark value when a trial ends"""
        self.MarkVal = 0
        self.MarkLabel.set("Mark: " + str(self.MarkVal))

    def addDataPoints(
        self,
        x_Time,
        data0,  # rightTorque
        data1,  # rightState
        data2,  # rightSet
        data3,  # leftTorque
        data4,  # leftState
        data5,  # leftSet
        data6,  # rightFsr
        data7,  # leftFsr
        data8,  # rightHeelFsr
        data9,  # leftHeelFsr
        data10, # rightAnkleAngle
        data11, # leftAnkleAngle
        data12,  # minSV
        data13,  # maxSV
        data14,  # minSA
        data15,  # maxSA
        data17,  # maxFSR
        data18,  # stancetime
        data19,  # swingtime
        Task,
        data16,  # Battery
    ):
        timestamp = int(datetime.now().timestamp())  # Current epoch time
        self.epochTime.append(timestamp)  # New list for epoch time
        self.tStep.append(x_Time)
        self.rTorque.append(data0)  # rightTorque
        self.rSetP.append(data2)  # rightSet
        self.rState.append(data1)  # rightState
        self.lTorque.append(data3)  # leftTorque
        self.lSetP.append(data5)  # leftSet
        self.lState.append(data4)  # leftState
        self.lFsr.append(data7)  # leftFsr
        self.rFsr.append(data6)  # rightFsr
        self.rHeelFsr.append(data8) # rightHeelFsr
        self.lHeelFsr.append(data9) # leftHeelFsr
        self.rAnkleAngle.append(data10) # rightAnkleAngle
        self.lAnkleAngle.append(data11) # leftAnkleAngle
        self.MinShankVel.append(data12)  # MinSV
        self.MaxShankVel.append(data13)  # MaxSV
        self.MinShankAng.append(data14)  # MinSA
        self.MaxShankAng.append(data15)  # MaxSA
        self.MaxFSR.append(data17)  # maxFSR
        self.StanceTime.append(data18)  # stanceTime
        self.SwingTime.append(data19)  # swingTime
        self.Task.append(Task)
        
        # Check for low battery indicator (-1)
        if data16 == -1:
            self.BatteryPercent.set("Low Batt")  # Display low battery warning
            self.battery_is_low = True
        else:
            self.BatteryPercent.set(f"Battery: {data10:.2f}V")  # Battery displayed as float with 2 decimal places
            self.battery_is_low = False
            
        self.Mark.append(self.MarkVal)
        