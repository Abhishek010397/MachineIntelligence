import json
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRTU
from Logger.LoggerHandling import Logging
import sys
from collections import deque

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
            Logging.logger.info("{} function has been called".format("getdevicesettings()"))
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
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
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
            Logging.logger.info("{} function has been called".format("getdeviceinfo()"))
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
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
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
            Logging.logger.info("{} function has been called".format("userdatablock()"))
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
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
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
            Logging.logger.info("{} function has been called".format("ConnectionType()"))
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
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
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
            Logging.logger.info("{} function has been called".format("Get_polling_freq()"))
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
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            f.close()

    def Tcp_function(self, device_setting): 
        """
            This function Loads the device_setting Parameter to get Connection Related information

            :param Tcp_function: device_setting
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns IPAddress and Port Number
            :rtype: String,int

        """

        try:
            Logging.logger.info("{} function has been called".format("Tcp_function()"))
            device_setting_json_value = json.loads(device_setting)
            IPAddress_value = device_setting_json_value["IPAddress"]
            Port_value = device_setting_json_value["Port"]
        except IOError:
            raise FileNotFoundError('File Not Found')
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return (IPAddress_value, Port_value)

    def RTU_function(self, device_setting):
        """
            This function Loads the device_setting Parameter to get Connection Related information

            :param RTU_function: device_setting
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns RTU Connection Related Information
            :rtype: tuple

        """

        try:
            Logging.logger.info("{} function has been called".format("RTU_function()"))
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return (client)
            

    def getdevicename(self):
        """
            This function Loads the modbus_config.json file and returns the Device Name

            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns Device Name
            :rtype: string

        """
        try:
            Logging.logger.info("{} function has been called".format("getdevicename()"))
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
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return (int(device_setting_unpack['UnitID']), int(DeviceInfoBlock_unpack['RegisterNumber'][0]), int(len(DeviceInfoBlock_unpack['RegisterNumber'])))

    def GetAllKeysFrom_DeviceInfoBlock(self, DeviceInfoBlock):
        """
            This function Loads DeviceInfoBlock information

            :param GetAllKeysFrom_DeviceInfoBlock: DeviceInfoBlock
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns information out of DeviceInfoBlock Parameter
            :rtype: tuple
        """
        try:
            Logging.logger.info("{} function has been called".format("GetAllKeysFrom_DeviceInfoBlock()"))
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return (RegisterNumber, RegisterName, RegisterType, DataType, Active)

    def dataTypeResponse(self, decoder, datatype_value):
        """
            This function Decodes Decoder Response using Inbuilt Functions based on Data Type via dataTypeResponse() function using decoder and datatype_value as parameter

            :param dataTypeResponse: it takes decoder and datatype_value as input
            :raises TypeError: If Error occurs in decoding the Decoder Object, it will raise Error
            :return: it returns Decoding typecasted data type values
            :rtype: string
        """
        try:
            Logging.logger.info("{} function has been called".format("dataTypeResponse()"))
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
        except IOError:
            raise TypeError('TypeError')
        except TypeError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            pass

    def GetAllKeysFrom_UserDataBlock1(self, UserDataBlock1):
        """
            This function returns all values specific to UserDataBlock1 Parameter(RegisterNumber,Multiplier etc)

            :param GetAllKeysFrom_UserDataBlock1: it takes UserDataBlock1 as input
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns values specific to UserDataBlock1 parameter
            :rtype: tuple
        """
        try:
            Logging.logger.info("{} function has been called".format("GetAllKeysFrom_UserDataBlock1()"))
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return (RegisterNumber, RegisterName, RegisterType, DataType, Active, Multiplier, Unit, DataRangeMin, DataRangeMax)

    def keys_get_function(self):
        """
            This function returns all Block Keys and values Related to DeviceID

            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns Data Block keys and values specific to Device id 
            :rtype: json
        """
        try:
            Logging.logger.info("{} function has been called".format("keys_get_function()"))
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
        except IOError:
            raise FileNotFoundError('File Not Found')
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
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
            Logging.logger.info("{} function has been called".format("keys_get_function()"))
            device_setting_unpack = json.loads(device_setting)
        except IOError:
            raise FileNotFoundError('File Not Found')
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return (int(device_setting_unpack['UnitID']))

    def DataCheckStatus(self, RegData, dict_values_of_k):
        """
            This function will check if The data lies within in a given range or Not

            :param DataCheckStatus: RegData and dict_values_of_userBlock
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it returns Offset, Length and UnitID
            :rtype: bool

        """
        flag = 0
        try:
            Logging.logger.info("{} function has been called".format("DataCheckStatus()"))
            for register_number_value in range(len(dict_values_of_k["RegisterNumber"])):
                if(register_number_value>=len(RegData)):
                    flag+=1
                    continue
                elif(int(RegData[register_number_value]) >= float(dict_values_of_k["DataRangeMin"][register_number_value]) and RegData[register_number_value] <= float(dict_values_of_k["DataRangeMax"][register_number_value])):
                    flag += 1
                    continue
                else:
                    flag = 0
                    break
        except IOError:
            raise TypeError("TypeError")
        except TypeError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            if(flag == 0):
                Logging.logger.error("check the data in range: Invalid Data")
                return (False)
            else:
                return (True)

    def DataResponseValidation(self, datatype_response, RegisterName_indexing, dict_values_of_k):
        """
            This function will check if The data lies within in a given range or Not

            :param DataResponseValidation: `datatype_response` , `RegisterName_indexing` and `dict_values_of_k`
            :raises IOError: If Error Occurs in Loading the json file,it will raise Error
            :return: it checks and return Boolean value if datatype_response is equal to RegisterData Value
            :rtype: bool

        """
        flag = 0
        try:
            Logging.logger.info("{} function has been called".format("DataResponseValidation()"))
            if(datatype_response >= float(dict_values_of_k["DataRangeMin"][RegisterName_indexing]) and datatype_response <= float(dict_values_of_k["DataRangeMax"][RegisterName_indexing]) ):
                flag = 1
            else:
                flag = 0
        except IOError:
            Logging.logger.exception(TypeError)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            if(flag == 0):
                return (False)
            else:
                return (True)

    def JsonValidation(self):

        """
            This function will check if the Json file is valid or Not and Device Id which user 
            has provided is present in Json file or not

            :raises IOError,FileNotFoundError: If Error Occurs in Loading the json file,it will raise Error or Block is present or not
            :return: it checks and return True if Json is valid is and all blocks are present else eturns False
            :rtype: bool

        """
        flag=0
        value=0
        try:
            Logging.logger.info("{} function has been called".format("JsonValidation()"))
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
        except IOError:
            Logging.logger.exception(TypeError)
        except TypeError as e:
            Logging.logger.exception(e)
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)    
        finally:
            f.close()
            if(flag==3):
                return (True)
            else:
                return (False)
        
    def Response_validation(self,key_pair_values,response,RegData, input_List):

        """
            This function will check if The data lies within in a given range or Not

            :param Response_validation: `key_pair_values` , `response` , `RegData` , `input_List`
            :raises Exception: AttributeError or TypeError
            :return: it checks and return True if data written into Register is equal to the Data read from the Register else False
            :rtype: bool

        """
        try:
            Logging.logger.info("{} function has been called".format("Response_validation()"))
            flag=0
            output=None
            indx=0
            for input_values in input_List:
                for k, v in key_pair_values.items():
                    if (input_values == k):
                        dict_values_of_k = v[0]
                        if(dict_values_of_k["RegisterType"][0]=="Read"):
                            flag=1
                        else:
                            for response_key,response_value in response.items():
                                if(input_values==response_key):
                                    for response_key2,response_value2 in response_value.items():
                                        index_response_key2=dict_values_of_k["RegisterName"].index(response_key2)
                    
                                        multiplier_RegData_value=round(RegData[index_response_key2]*eval(dict_values_of_k["Multiplier"][index_response_key2]),3)
                                        if(multiplier_RegData_value in RegData):
                                            flag=1
                                            continue
                                        else:
                                            flag=0
                                            raise Exception
        except IOError:
            Logging.logger.exception(TypeError)
        except TypeError as e:
            Logging.logger.exception(e)
        except FileNotFoundError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            if(flag==1):
                return (True)
            else:
                return(False)
    
    def Data_to_be_written(self,RegData,dict_values_of_k): 

        """
            This function will return the Set of values to be written into Respective Registers

            :param Response_validation: `dict_values_of_k`, `RegData` 
            :raises Exception: AttributeError or TypeError
            :return: it checks and returns the set of Data to be written into Registers
            :rtype: list

        """

        q=deque()
        lst=[]
        lst1=[]
        length=len(dict_values_of_k["RegisterNumber"])

        if(len(RegData)>=length):
            for data_value in range(len(RegData)): 
                q.append(RegData[data_value])
        else:
            for data_value in range(length):
                if(data_value>=len(RegData)):
                    q.append(0)
                else:
                    q.append(RegData[data_value])
                    
        for data_value in range(length):
            lst.append(q.popleft())

        queue_size=len(q)
        if(queue_size==0):
            lst1.append(0)
        else:
            for left_values in range(queue_size):
                lst1.append(q.popleft())
        return (lst,lst1)
