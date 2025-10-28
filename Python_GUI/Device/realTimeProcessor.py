import re

from Device import chart_data, exoData, MLModel


class RealTimeProcessor:
    def __init__(self):
        self._event_count_regex = re.compile(
            "[0-9]+"
        )  # Regular Expression to find any number 1-9
        self._start_transmission = False
        self._command = None
        self._num_count = 0
        self._buffer = []
        self._payload = []
        self._result = ""
        self._exo_data = exoData.ExoData()
        self._chart_data = chart_data.ChartData()
        self._data_length = None
        self.x_time = 0
        self._predictor= MLModel.MLModel() #create the machine learning model object
        

    def processEvent(self, event):
        # Decode data from bytearry->String
        dataUnpacked = event.decode("utf-8")
        if "c" in dataUnpacked:  # 'c' acts as a delimiter for data
            data_split = dataUnpacked.split(
                "c"
            )  # Split data into 2 messages using 'c' as divider
            event_data = data_split[1]  # Back half of split holds message data
            # Front half of split holds message information
            event_info = data_split[0]
            count_match = self._event_count_regex.search(
                event_info
            ).group()  # Look for data count described in data info
            self._data_length = int(count_match)
            start = event_info[0]  # Start of data
            cmd = event_info[1]  # Command the data holds
            # Data without the count
            event_without_count = f"{start}{cmd}{event_data}"
            # Parse the data and handle each part accordingly
            for element in event_without_count:
                if (
                    element == "S" and not self._start_transmission
                ):  # 'S' signifies that start of the message
                    self._start_transmission = True
                    continue  # Keep reading message
                elif self._start_transmission:  # if the message has started
                    if not self._command:
                        self._command = element  # if command is empty, set command to current element
                    elif element == "n":
                        self._num_count += 1  # Increase the num count of message
                        # Join the buffer to result
                        result = "".join(self._buffer)
                        double_parse = tryParseFloat(
                            result
                        )  # Parse the result and convert to double if possible, None if not possible
                        if double_parse is None:
                            continue  # Keep reading message
                        else:
                            self._payload.append(
                                double_parse / 100.0
                            )  # Add data to payload
                            self._buffer.clear()
                            if (
                                self._num_count == self._data_length
                            ):  # If the data length is equal to the data count
                                self.processMessage(
                                    self._command, self._payload, self._data_length
                                )
                                self._reset()  # Reset message variables for a new message
                            else:
                                continue  # Keep reading message
                    elif self._data_length != 0:
                        self._buffer.append(element)  # Add data to buffer
                    else:
                        return
                else:
                    return
        else:
            print("Unkown command!\n")

    def set_debug_event_listener(self, on_debug_event):
        self._on_debug_event = on_debug_event

    def processGeneralData(
        self, payload, datalength
    ):  # Place general data derived from message to Exo data
        # print("Payload:", payload)
        # print("Len:", len(payload))
        # print("datalength:", datalength)
                
        self.x_time += 1
        data0 = payload[0] if len(payload) > 1 else 0  # right_side.ankle.controller.filtered_torque_reading
        data1 = payload[1] if len(payload) > 2 else 0  # right_side.ankle.controller.ff_setpoint
        data2 = payload[2] if len(payload) > 3 else 0  # left_side.ankle.controller.filtered_torque_reading
        data3 = payload[3] if len(payload) > 4 else 0  # left_side.ankle.controller.ff_setpoint
        data4 = payload[4] if len(payload) > 5 else 0  # right_side.toe_stance
        data5 = payload[5] if len(payload) > 6 else 0  # right_side.toe_fsr
        data6 = payload[6] if len(payload) >= 7 and len(payload) > 6 else 0  # left_side.toe_stance
        data7 = payload[7] if len(payload) >= 8 and len(payload) > 7 else 0  # left_side.toe_fsr
        data8 = payload[8] if len(payload) >= 9 and len(payload) > 8 else 0  # right_side.heel_fsr
        data9 = payload[9] if len(payload) >= 10 and len(payload) > 9 else 0  # left_side.heel_fsr
        data10 = payload[10] if len(payload) >= 11 and len(payload) > 10 else -1  # right_side.ankle.joint_position        
        data11 = payload[11] if len(payload) >= 12 and len(payload) > 11 else 1  # left_side.ankle.joint_position        
        data12 = payload[12] if len(payload) >= 13 and len(payload) > 12 else 0  # minSV 
        data13 = payload[13] if len(payload) >= 14 and len(payload) > 13 else 0  # maxSV
        data14 = payload[14] if len(payload) >= 15 and len(payload) > 14 else 0  # minSA
        data15 = payload[15] if len(payload) >= 16 and len(payload) > 15 else 0  # maxSA
        data16 = payload[16] if len(payload) >= 17 and len(payload) > 16 else 0  # battery
        data17 = payload[17] if len(payload) >= 18 and len(payload) > 17 else 0  # maxFSR
        data18 = payload[18] if len(payload) >= 19 and len(payload) > 18 else 0  # stancetime
        data19 = payload[19] if len(payload) >= 20 and len(payload) > 19 else 0  # swingtime
        


        self._chart_data.updateValues(
            data0,  # rightTorque
            data1,  # rightSet
            data2,  # leftTorque
            data3,  # leftSet
            data4,  # right_side.toe_stance
            data5,  # right_side.toe_fsr
            data6,  # left_side.toe_stance
            data7,  # left_side.toe_fsr
            data8,  # rightHeelFsr
            data9,  # leftHeelFsr
            data10, # rightAnkleAngle
            data11, # leftAnkleAngle
            data12,  # minSV
            data13,  # maxSV
            data14,  # minSA
            data15,  # maxSA
            data16,  # battery
            data17,  # maxFSR
            data18,  # stancetime
            data19,  # swingtime
        )
        
        self._predictor.addDataPoints([data12, data13, data14, data15, data17, data18, data19, self._predictor.state]) #add data to model, if recording data (using minSA=data12)
        
        self._predictor.predictModel([data12, data13, data14, data15, data17, data18, data19]) #predict results from model (using minSA=data12)


        self._exo_data.addDataPoints(
            self.x_time,
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
            #store features
            data12,  # minSV
            data13,  # maxSV
            data14,  # minSA
            data15,  # maxSA
            data17,  # maxFSR
            data18,  # stancetime
            data19,  # swingtime
            self._predictor.prediction, #store prediction
            data16  # battery
        )
        

    def processMessage(
        self, command, payload, dataLength
    ):  # Process message based on command. Only handles general data although other data is comming through
        if command == "?":  # General command
            self.processGeneralData(payload, dataLength)

    def _reset(self):  # Reset message variables
        self._start_transmission = False
        self._command = None
        self._data_length = None
        self._num_count = 0
        self._payload.clear()
        self._buffer.clear()

    def UnkownDataCommand(self):
        return "Unkown Command!"


def tryParseFloat(stringVal):  # Try to parse float data from String
    try:
        return float(stringVal)  # If possible, return parsed
    except:
        return None  # If not, return None
