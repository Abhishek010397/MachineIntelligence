import json
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRTU
from LoggerHandling import Logging
import sys

class Modbusconfigjsondecoder:

    """
    This is a Conceptual class Responsible for Defining every functionality needed to get the Information Out of It(Json File).

    :param DeviceID: This class takes DeviceID as Parameter (For instantiation) and Stores the response in DeviceID for further use
    :type DeviceID: int

    """

    def __init__(self, DeviceID):
        """
            Constructor Method
        """
        self.DeviceID = DeviceID

    def getdevicesettings(self):
        """
            This function Loads the modbus_config.json file and returns the DeviceSettings information in json format

            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: It returns the Json object(DeviceSettings information)
            :rtype: Json

        """
        try:
            '''
            Loading the modbus_config.json file
            '''
            f = open('modbus_config.json', 'r')
            json_object=None
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2, v2 in v.items():
                            if(k2 == "DeviceSettings"):
                                value = v2[0]
                                json_object = json.dumps(value)
                                break
                    break
                else:
                    Logging.logger.info("DeviceID not present")
        except IOError:
            raise FileNotFoundError('File Not Found')
        finally:
            f.close()
            return (json_object)

    def getdeviceinfo(self):
        """
            This function Loads the modbus_config.json file and returns the getdeviceinfo information in json format

            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: It returns the Json object(getdeviceinfo information)
            :rtype: Json

        """
        try:
            '''
            Loading the modbus_config.json file
            '''
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        finally:
            f.close()

    def userdatablock(self):
        """
            This function Loads the modbus_config.json file and returns the userdatablock information in json format

            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: It returns the Json object(userdatablock information)
            :rtype: Json

        """
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        finally:
            f.close()

    def ConnectionType(self):
        """
            This function Loads the modbus_config.json file and returns the ConnectionType information

            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: It returns the Connection Type(TCP,RTU)
            :rtype: String

        """
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        finally:
            f.close()

    def Get_polling_freq(self):
        """
            This function Loads the modbus_config.json file and returns the Polling Frequency information

            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns Polling Frequency for Each DeviceID
            :rtype: int

        """
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2, v2 in v.items():
                            if(k2 == "PollingRate"):
                                return (int(v2.split()[0]))
        except IOError:
            raise FileNotFoundError('File Not Found')
        finally:
            f.close()

    def Tcp_function(self, device_setting):  # private
        """
            This function Loads the device_setting Parameter to get Connection Related information

            :param Tcp_function: device_setting
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns IPAddress and Port Number
            :rtype: String,int

        """

        try:
            device_setting_json_value = json.loads(device_setting)
            IPAddress_value = device_setting_json_value["IPAddress"]
            Port_value = device_setting_json_value["Port"]
            return (IPAddress_value, Port_value)
        except IOError:
            raise FileNotFoundError('File Not Found')

    def RTU_function(self, device_setting):  # make it private
        """
            This function Loads the device_setting Parameter to get Connection Related information

            :param RTU_function: device_setting
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns RTU Connection Related Information
            :rtype: tuple

        """

        try:
            device_setting_json_value = json.loads(device_setting)
            client = ModbusClientRTU(
                method='rtu',
                port=str(device_setting_json_value['rtuPort']),
                baudrate=int(device_setting_json_value['BaudRate']),
                timeout=int(device_setting_json_value['timeout']),
                parity=str(device_setting_json_value['Parity']),
                stopbits=int(device_setting_json_value['StopBit']),
                bytesize=int(device_setting_json_value['bytesize'])
            )
            return (client)
        except IOError:
            raise FileNotFoundError('File Not Found')

    def getdevicename(self):
        """
            This function Loads the modbus_config.json file and returns the Device Name

            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns Device Name
            :rtype: string

        """
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        finally:
            f.close()

    def Offset_Length_Unitid(self, device_setting, dict_values_of_k):
        """
            This function Loads device_setting and DeviceInfoBlock information

            :param Offset_Length_Unitid: device_setting and DeviceInfoBlock
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns Offset, Length and UnitID
            :rtype: int,int,int

        """
        try:
            device_setting_unpack = json.loads(device_setting)
            DeviceInfoBlock_unpack = dict_values_of_k
            return (int(device_setting_unpack['UnitID']), int(DeviceInfoBlock_unpack['RegisterNumber'][0]), int(len(DeviceInfoBlock_unpack['RegisterNumber'])))
        except IOError:
            raise FileNotFoundError('File Not Found')

    def GetAllKeysFrom_DeviceInfoBlock(self, DeviceInfoBlock):
        """
            This function Loads DeviceInfoBlock information

            :param GetAllKeysFrom_DeviceInfoBlock: DeviceInfoBlock
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns information out of DeviceInfoBlock Parameter
            :rtype: tuple
        """
        try:
            DeviceInfoBlock_unpack = json.loads(DeviceInfoBlock)
            for k, v in DeviceInfoBlock_unpack.items():
                if(k == "RegisterNumber"):
                    RegisterNumber = v
                elif(k == "RegisterName"):
                    RegisterName = v
                elif(k == "RegisterType"):
                    RegisterType = v
                elif(k == "DataType"):
                    DataType = v
                elif(k == "Active"):
                    Active = v
            return (RegisterNumber, RegisterName, RegisterType, DataType, Active)
        except IOError:
            raise FileNotFoundError('File Not Found')

    def dataTypeResponse(self, decoder, datatype_value):
        """
            This function Decodes Decoder Response using Inbuilt Functions based on Data Type via dataTypeResponse() function using decoder and datatype_value as parameter

            :param dataTypeResponse: it takes decoder and datatype_value as input
            :raises TypeError: If Error occurs in decoding the Decoder Object, it will raise Error
            :return: it returns Decoding typecasted data type values
            :rtype: string
        """
        try:
            if(str(datatype_value) == "String32"):
                return (decoder.decode_string(32))
            elif(str(datatype_value) == "String"):
                return (decoder.decode_string(8))
            elif(str(datatype_value) == "String16"):
                return (decoder.decode_string(16))
            elif(str(datatype_value) == "16int" or str(datatype_value) == "int16" or str(datatype_value) == "16int"):
                return (decoder.decode_16bit_int())
            elif(str(datatype_value) == "32 bit int" or str(datatype_value) == "int32" or str(datatype_value) == "32int"):
                return (decoder.decode_32bit_int())
            elif(str(datatype_value) == "bits"):
                return (decoder.decode_bits())
            elif(str(datatype_value) == "8int" or str(datatype_value) == "int8"):
                return (decoder.decode_8bit_int())
            elif(str(datatype_value) == "8uint"):
                return (decoder.decode_8bit_uint())
            elif(str(datatype_value) == "16uint"):
                return (decoder.decode_16bit_uint())
            elif(str(datatype_value) == "32uint"):
                return (decoder.decode_32bit_uint())
            elif(str(datatype_value) == "16float" or str(datatype_value) == "16float2"):
                return (decoder.decode_16bit_float())
            elif(str(datatype_value) == "32float" or str(datatype_value) == "32float2"):
                return (decoder.decode_32bit_float())
            elif(str(datatype_value) == "64uint"):
                return (decoder.decode_64bit_uint())
            elif(str(datatype_value) == "ignore"):
                return (decoder.skip_bytes(8))
            elif(str(datatype_value) == "64float" or str(datatype_value) == "64float2"):
                return (decoder.decode_64bit_float())

        except IOError:
            raise TypeError

    def GetAllKeysFrom_UserDataBlock1(self, UserDataBlock1):
        """
            This function returns all values specific to UserDataBlock1 Parameter(RegisterNumber,Multiplier etc)

            :param GetAllKeysFrom_UserDataBlock1: it takes UserDataBlock1 as input
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns values specific to UserDataBlock1 parameter
            :rtype: tuple
        """
        try:
            UserDataBlock1_unpack = json.loads(UserDataBlock1)
            for k, v in UserDataBlock1_unpack.items():
                if(k == "RegisterNumber"):
                    RegisterNumber = v
                elif(k == "RegisterName"):
                    RegisterName = v
                elif(k == "RegisterType"):
                    RegisterType = v
                elif(k == "DataType"):
                    DataType = v
                elif(k == "Active"):
                    Active = v
                elif(k == "Multiplier"):
                    Multiplier = v
                elif(k == "Unit"):
                    Unit = v
                elif(k == "DataRangeMin"):
                    DataRangeMin = v
                elif(k == "DataRangeMax"):
                    DataRangeMax = v
            return (RegisterNumber, RegisterName, RegisterType, DataType, Active, Multiplier, Unit, DataRangeMin, DataRangeMax)
        except IOError:
            raise FileNotFoundError('File Not Found')

    def keys_get_function(self):
        try:
            d = {}
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
                                            d[k2] = v2
            # return (d)
        except IOError:
            raise FileNotFoundError('File Not Found')
        finally:
            f.close()
            return (d)

    def Unitid_singleWrite(self, device_setting, dict_values_of_k):
        """
            This function Loads device_setting and DeviceInfoBlock information

            :param Unitid_singleWrite: device_setting and dict_values_of_k
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns Offset, Length and UnitID
            :rtype: int

        """
        try:
            device_setting_unpack = json.loads(device_setting)
            return (int(device_setting_unpack['UnitID']))
        except IOError:
            raise FileNotFoundError('File Not Found')

    def DataCheckStatus(self, RegData, dict_values_of_k):
        """
            This function will check if The data lies within in a given range or Not

            :param DataCheckStatus: RegData and dict_values_of_userBlock
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns Offset, Length and UnitID
            :rtype: bool

        """
        flag = 0
        # self.RegData = RegData
        # self.dict_values_of_k = dict_values_of_k
        try:
            for register_number_value in range(len(dict_values_of_k["RegisterNumber"])):
                if(int(RegData[register_number_value]) >= float(dict_values_of_k["DataRangeMin"][register_number_value]) and RegData[register_number_value] <= float(dict_values_of_k["DataRangeMax"][register_number_value])):
                    flag += 1
                    continue
                else:
                    flag = 0
                    break
        except IOError:
            raise TypeError
        finally:
            if(flag == 0):
                Logging.logger.info("check the data in range: Invalid Data")
                return (False)
            else:
                return (True)

    def DataResponseValidation(self, datatype_response, RegisterName_indexing, dict_values_of_k):
        """
            This function will check if The data lies within in a given range or Not

            :param DataCheckStatus: datatype_response and RegisterName_indexing
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it checks and return Boolean value if datatype_response is equal to RegisterData Value
            :rtype: bool

        """
        flag = 0
        try:
            if(datatype_response >= float(dict_values_of_k["DataRangeMin"][RegisterName_indexing]) and datatype_response <= float(dict_values_of_k["DataRangeMax"][RegisterName_indexing])):
                flag = 1
            else:
                flag = 0
        except IOError:
            Logging.logger.info(TypeError)
        finally:
            if(flag == 0):
                return (False)
            else:
                return (True)

    def JsonValidation(self):

        """
            This function will check if The data lies within in a given range or Not

            :param DataCheckStatus: datatype_response and RegisterName_indexing
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it checks and return Boolean value if datatype_response is equal to RegisterData Value
            :rtype: bool

        """
        flag=0
        value=0
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1, v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k3,v3 in v.items():
                            if(k3=="DeviceSettings" and v1 == self.DeviceID):
                                flag=flag+1
                                continue
                            elif(k3=="PollingRate" and v1 == self.DeviceID):
                                flag=flag+1
                                continue
                            elif(k3=="DeviceType" and v1 == self.DeviceID):
                                value=str(v["DeviceType"])
                                flag+=1
                                continue
                    
            if(flag>=3):
                flag=0
                for k,v in data.items():
                    if(k==str(value)):
                        for k2,v2 in v.items():
                            if(k2=="ConnType" and k==str(value)):
                                flag+=1
                            elif(k==str(value) and k2=="DeviceInfoBlock"):
                                flag+=1
                            elif(k==str(value) and k2=="UserDataBlock1"):
                                flag+=1
        except Exception as e:
            Logging.logger.info(e)
        finally:
            f.close()
            if(flag==3):
                return (True)
            else:
                return (False)
	


