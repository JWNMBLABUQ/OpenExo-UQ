class ChartData:
    def __init__(self):
        self.data0 = 0.0  # rightTorque
        self.data1 = 0.0  # rightState
        self.data2 = 0.0  # rightSet
        self.data3 = 0.0  # leftTorque
        self.data4 = 0.0  # leftState
        self.data5 = 0.0  # leftSet
        self.data6 = 0.0  # rightToeFsr
        self.data7 = 0.0  # leftToeFsr
        self.data8 = 0.0  # rightHeelFsr
        self.data9 = 0.0  # leftHeelFsr
        self.data10 = 0.0  # rightAnkleAngle
        self.data11 = 0.0  # leftAnkleAngle
        self.data12 = 0.0  # minSV
        self.data13 = 0.0  # maxSV
        self.data14 = 0.0  # minSA
        self.data15 = 0.0  # maxSA
        self.data16 = 0.0  # battery
        self.data17 = 0.0  # maxFSR
        self.data18 = 0.0  # stancetime
        self.data19 = 0.0  # swingtime  
        
    def updateValues(
        self,
        data0,  # rightTorque
        data1,  # rightState
        data2,  # rightSet
        data3,  # leftTorque
        data4,  # leftState
        data5,  # leftSet
        data6,  # rightToeFsr
        data7,  # leftToeFsr
        data8,  # rightHeelFsr
        data9,  # leftHeelFsr
        data10, # rightAnkleAngle
        data11, #leftAnkleAngle
        data12,  # minSV
        data13,  # maxSV
        data14,  # minSA
        data15,  # maxSA
        data16,  # battery
        data17,  # maxFSR
        data18,  # stancetime
        data19,  # swingtime      
    ):
        self.data0 = data0
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.data4 = data4
        self.data5 = data5
        self.data6 = data6
        self.data7 = data7
        self.data8 = data8
        self.data9 = data9
        self.data10 = data10
        self.data11 = data11
        self.data12 = data12
        self.data13 = data13
        self.data14 = data14
        self.data15 = data15
        self.data16 = data16
        self.data17 = data17
        self.data18 = data18
        self.data19 = data19
