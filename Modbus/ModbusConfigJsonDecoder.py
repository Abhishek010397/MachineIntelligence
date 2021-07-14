import json
from collections import namedtuple
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRTU


class Modbusconfigjsondecoder:
    def __init__(self, DeviceID):
        self.DeviceID = DeviceID

    def getdevicesettings(self):
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2, v2 in v.items():
                            if(k2 == "DeviceSettings"):
                                value = v2[0]
                                json_object = json.dumps(value)
                                return (json_object)

        except Exception as e:
            print(e)

    def getdeviceinfo(self):
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2, v2 in v.items():
                            if(k2 == "DeviceType"):
                                value = v["DeviceType"]
                                for k, v in data.items():
                                    if(k == str(value)):
                                        for k2, v2 in v.items():
                                            if(k2 == "DeviceInfoBlock"):
                                                value = v2[0]
                                                return (json.dumps(value, indent=4))
        except Exception as e:
            print(e)

    def userdatablock(self):
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2, v2 in v.items():
                            if(k2 == "DeviceType"):
                                value = v["DeviceType"]
                                for k, v in data.items():
                                    if(k == str(value)):
                                        for k2, v2 in v.items():
                                            if(k2 == "UserDataBlock1"):
                                                value = v2[0]
                                                return (json.dumps(value, indent=4))
        except Exception as e:
            print(e)

    def ConnectionType(self):
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2, v2 in v.items():
                            if(k2 == "DeviceType"):
                                value = v["DeviceType"]
                                for k, v in data.items():
                                    if(k == str(value)):
                                        for k2, v2 in v.items():
                                            if(k2 == "ConnType"):
                                                return (v2)
        except Exception as e:
            print(e)

    def Get_polling_freq(self):
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2, v2 in v.items():
                            if(k2 == "PollingRate"):
                                return (int(v2.split()[0]))
        except Exception as e:
            print(e)

    def Tcp_function(self, device_setting):

        try:
            device_setting_json_value = json.loads(device_setting)
            IPAddress_value = device_setting_json_value["IPAddress"]
            Port_value = device_setting_json_value["Port"]
            return (IPAddress_value, Port_value)
        except Exception as e:
            print(e)

    def RTU_function(self, device_setting):

        try:
            device_setting_json_value = json.loads(device_setting)
            ModbusClientRTU = namedtuple('ModbusClientRTU', [
                                         'method', 'rtuPort', 'BaudRate', 'timeout', 'Parity', 'StopBit', 'bytesize'])
            client = ModbusClientRTU(
                method='rtu',
                rtuPort=str(device_setting_json_value['rtuPort']),
                BaudRate=str(device_setting_json_value['BaudRate']),
                timeout=str(device_setting_json_value['BaudRate']),
                Parity=str(device_setting_json_value['Parity']),
                StopBit=str(device_setting_json_value['StopBit']),
                bytesize=str(device_setting_json_value['bytesize'])
            )
            return (client)
        except Exception as e:
            print(e)

    def getdevicename(self):
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2, v2 in v.items():
                            if(k2 == "DeviceType"):
                                value = v["DeviceType"]
                                for k, v in data.items():
                                    if(k == str(value)):
                                        for k2, v2 in v.items():
                                            if(k2 == "DeviceName"):
                                                return (str(v2))
        except Exception as e:
            print(e)

    def Offset_Length_Unitid(self, device_setting, DeviceInfoBlock):
        try:
            device_setting_unpack = json.loads(device_setting)
            DeviceInfoBlock_unpack = json.loads(DeviceInfoBlock)
            return (int(device_setting_unpack['UnitID']), int(DeviceInfoBlock_unpack['RegisterNumber'][0]), int(len(DeviceInfoBlock_unpack['RegisterNumber'])))

        except Exception as e:
            print(e)




   

    
    







        







