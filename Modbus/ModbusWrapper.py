from struct import pack, unpack, error
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ModbusIOException, ParameterException, ConnectionException
from pymodbus.payload import BinaryPayloadDecoder
import json
from pymodbus.constants import Endian
from Modbus.ModbusConfigJsonDecoder import Modbusconfigjsondecoder
from Logger.LoggerHandling import Logging
from Modbus.UtilityClass import Decoder
import re

class Modbus:
    """
    This is a Conceptual class Responsible for Fetching every information Related to DeviceID

    :param DeviceID: This class takes DeviceID as Parameter. It instantiate Modbusconfigjsondecoder class and save the response in `device object`
    :type DeviceID: int

    """

    def __init__(self, DeviceID):

        """
        Constructor method
        """
        self.DeviceID=DeviceID
        self.device = Modbusconfigjsondecoder(self.DeviceID)
        self.value_parsing= Decoder()

    def polling_freq(self):
        """ This function calls the Get_polling_freq() function defined in Modbusconfigjsondecoder Module to get the poll_frequency

        :return: poll_frequency for each deviceID
        :rtype: int

        """
        try:
            Logging.logger.info("Calling {} function".format("Get_polling_freq()"))
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            poll_frequency = self.device.Get_polling_freq()
            return (poll_frequency)

    def connect_function(self):
        """
        This function checks the connection Type and accordingly call the function(Tcp_function() or RTU_function()) to get Connection Related Information

        :raises ConnectionError: If connection does not get connected to Server, it will raise Error
        :return: It returns `Device_connection_master` and `device_connector`
        :rtype: `Device_connection_master` object and `True` if device_connector is connected to Server otherwise `False`

        """

        try:
            Logging.logger.info("Running connect_function")
            connect_type = self.device.ConnectionType()
            if (connect_type == "TCP"):

                IPAddress_value, Port_value = self.device.Tcp_function(self.device.getdevicesettings())
                Device_connection_master = ModbusClient(IPAddress_value, int(Port_value))
                device_connector = Device_connection_master.connect()
                return (Device_connection_master, device_connector)
            elif (connect_type == "RTU"):

                Device_connection_master = self.device.RTU_function(self.device.getdevicesettings())
                device_connector = Device_connection_master.connect()
                return (Device_connection_master, device_connector)
        except Exception as e:
            Logging.logger.exception(e, exc_info=True)

    def modbus_block_read(self, input_list):
        """
            This function returns every values what we write into `register`. it gets the values values from connect_function() and checks if Connection is `True`. It iterates through input_list and accordingly returns Values in Json format via functions defined in ModbusConfigJsonDecoder Module

            :param modbus_block_read: input_list passed from ModbusPolling Module
            :raises ModbusIOException,ParameterException,ConnectionException: when either of the Exceptions occur, it will taise Errors
            :return: Json object
            :rtype: json
        """
        try:
            final_json_data = {}
            if(self.device.JsonValidation()==True):
                pass
            else:
                Logging.logger.warning("DeviceID absent, please check")
                raise AttributeError
            Device_connection_master, device_connector = self.connect_function()
            '''
            Checking if My Connection has Connected to Server 
            '''
            print(Device_connection_master, device_connector)
            if (device_connector == True):
                '''
                Iterating through input_list to return data Accordingly
                '''
                key_pair_values = self.device.keys_get_function()
                if(not input_list):
                    for k, v in key_pair_values.items():
                        final_json_data[k] = v    
                else:
                    for input_values in input_list:
                        nested_json_data = {}
                        for k, v in key_pair_values.items():
                            if (input_values == k):
                                if(input_values=="DeviceInfoBlock"):
                                    dict_values_of_k = v[0]
                                    unitId, offset, length = self.device.Offset_Length_Unitid(self.device.getdevicesettings(),dict_values_of_k)
                                    # print(unitId, offset, length)
                                    res = Device_connection_master.read_holding_registers(offset, 10, unit=unitId)
                                    decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder=Endian.Big)
                                    x1=decoder.decode_string(32)
                                    x1=x1.decode("utf-8")
                                    start,end=0,0
                                    for RegisterName_indexing in range(len(dict_values_of_k["RegisterName"])):
                                        nested_json_data[str(dict_values_of_k["RegisterName"][RegisterName_indexing])]=x1[start:end+2]
                                        start=end+2
                                        end=5
                                    final_json_data[str(input_values)] = dict(nested_json_data)
                                    del nested_json_data 
                                else:
                                    dict_values_of_k = v[0]
                                    unitId, offset, length = self.device.Offset_Length_Unitid(self.device.getdevicesettings(),dict_values_of_k)
                                    # print(unitId, offset, length)
                                    response = Device_connection_master.read_holding_registers(offset, length, unit=unitId)
                                    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Big)

                                    for RegisterName_indexing in range(len(dict_values_of_k["RegisterName"])):

                                        datatype_response = self.device.dataTypeResponse(decoder, dict_values_of_k["DataType"][RegisterName_indexing])
                                        if(isinstance(datatype_response, float)==True):
                                            datatype_response=datatype_response
                                        else:
                                            """
                                            Parsing the Data using s16 function
                                            """
                                            datatype_response=self.value_parsing.s16(datatype_response)
                                        """
                                        Checking Validation of Data 
                                        """
                                        data_response_validation = self.device.DataResponseValidation(datatype_response,RegisterName_indexing,dict_values_of_k)
                                        if (data_response_validation == True):
                                            """
                                            Multiplying the Actual Data with Multiplier
                                            """
                                            nested_json_data[str(dict_values_of_k["RegisterName"][RegisterName_indexing])] = round((datatype_response)*(eval(dict_values_of_k["Multiplier"][RegisterName_indexing])), 3)
                                        # else:
                                        #     Logging.logger.error("Please check Data Range values, and fix that")

                                    final_json_data[str(input_values)] = dict(nested_json_data)
                                    del nested_json_data
            else:
                Logging.logger.exception(ConnectionError)
                raise ConnectionError

        except ModbusIOException as e:
            final_json_data={"error_code":101,"error_desc":"ModbusIOError"}
            Logging.logger.exception(e)
        except ParameterException as e:
            final_json_data={"error Code":102,"Error Desc":"ParameterError"}
            Logging.logger.exception(e)
        except ConnectionError as e:
            final_json_data={"error Code":103,"Error Desc":"ConnectionError"}
            Logging.logger.exception(e, exc_info=True)
        except AttributeError as e:
            final_json_data={"error Code":104,"Error Desc":"AttributeError"}
            Logging.logger.exception(e)
        except TypeError as e:
            final_json_data={"error Code":106,"Error Desc":"Type Error"}
            Logging.logger.exception(e)
        except Exception as e:
            final_json_data={"error Code":105,"Error Desc":"User Related Error"}
            Logging.logger.exception(e)
        finally:
            Device_connection_master.close()
            return (final_json_data)

    def modbus_single_write(self, RegData, input_List):

        """
            It will write into Register one by one via Iteration

            :param modbus_single_write: RegisterData and input_List
        """
        write_result=None
        RegData1=0
        lst=[]
        try:
            if(self.device.JsonValidation()==True):
                pass
            else:
                Logging.logger.warning("DeviceID absent, please check")
                raise AttributeError
            write_result_json={}
            Device_connection_master, device_connector = self.connect_function()
            if (device_connector == True):
                key_pair_values = self.device.keys_get_function()
                for input_values in input_List:
                    for k, v in key_pair_values.items():
                        if (input_values == k):
                            dict_values_of_k = v[0]
                            if(RegData1==0):
                                RegData,RegData1=self.device.Data_to_be_written(RegData,dict_values_of_k)
                            else:
                                RegData,RegData1=self.device.Data_to_be_written(RegData1,dict_values_of_k)
                            lst+=RegData
                            if(dict_values_of_k["RegisterType"][0].lower()=="read"):
                                Logging.logger.warning("Input_value {} is Read Data type,can't write into register".format(input_values)) 
                            else:
                                unitId = self.device.Unitid_singleWrite(self.device.getdevicesettings(), dict_values_of_k)
                                data_check_status = self.device.DataCheckStatus(RegData, dict_values_of_k)
                        
                                if (data_check_status == True):
                                    for register_number_value in range(len(dict_values_of_k["RegisterNumber"])):
                                        y=("".join(x for x in (re.findall("[a-zA-Z]",dict_values_of_k["DataType"][register_number_value]))).lower())
                                        if(y=="float"):
                                            print(self.device.write_into_float(float(RegData[register_number_value])))
                                            write_result = Device_connection_master.write_registers(
                                                int(dict_values_of_k["RegisterNumber"][register_number_value]),
                                                self.device.write_into_float(float(RegData[register_number_value])), unit=unitId,skip_encode=True)
                                        
                                            write_result_json[str(dict_values_of_k["RegisterNumber"][register_number_value])]=write_result
                                        else:
                                            write_result = Device_connection_master.write_registers(
                                                int(dict_values_of_k["RegisterNumber"][register_number_value]),
                                                self.value_parsing.signed(int(RegData[register_number_value])), unit=unitId)
                                        
                                            write_result_json[str(dict_values_of_k["RegisterNumber"][register_number_value])]=write_result
                                else:
                                    Logging.logger.warning("Can't Write Data into Register,Invalid Data")
                                    raise ValueError
            else:
                Logging.logger.exception(ConnectionError)
                raise ConnectionError
        except (ModbusIOException, error):
            write_result_json={"error Code":101,"Error Desc":"ModbusIOError"}
            Logging.logger.exception(error)
        except ParameterException as e:
            write_result_json={"error Code":102,"Error Desc":"Parameter Exception Error"}
            Logging.logger.exception(e)
        except ConnectionError as e:
            write_result_json={"error Code":103,"Error Desc":"Connection Error"}
            Logging.logger.exception(e)
        except AttributeError as e:
            write_result_json={"error Code":104,"Error Desc":"Attribute Error"}
            Logging.logger.exception(e)
        except TypeError as e:
            write_result_json={"error Code":105,"Error Desc":"Type Error"}
            Logging.logger.exception(e)
        except ValueError as e:
            write_result_json={"error Code":107,"Error Desc":"Value Error"}
            Logging.logger.exception(e)
        except Exception as e:
            write_result_json={"error Code":106,"Error Desc":"User Related Error"}
            Logging.logger.exception(e)
        finally:
            if(write_result==None):
                Logging.logger.info(write_result_json)
            else:
                if(dict_values_of_k["RegisterType"][0].lower()=="readwrite"):
                    if(write_result!=None):
                        response=self.modbus_block_read(input_List)
                        if(self.device.Response_validation(key_pair_values,response,lst, input_List)):
                            Logging.logger.info({"Read_Response":"Written and Reading data match perfectly"})
                        else:
                            Logging.logger.warning({"Read_Response":"Written Data does not match with Read data"})
                elif(dict_values_of_k["RegisterType"][0].lower()=="write"):
                    Logging.logger.info(write_result_json)
            Device_connection_master.close()

    def modbus_block_write(self, RegData, input_List):

        """
            It will write into Register block wise without Iterating

            :param modbus_block_write: RegisterData and input_List
        """
        RegData1=0
        lst=[]
        try:
            write_result=None
            if(self.device.JsonValidation()==True):
                pass
            else:
                Logging.logger.warning("DeviceID absent, please check")
                raise AttributeError
            write_result_json={}
            Device_connection_master, device_connector = self.connect_function()
            if (device_connector == True):
                key_pair_values = self.device.keys_get_function()
                for input_values in input_List:
                    for k, v in key_pair_values.items():
                        if (input_values == k):
                            dict_values_of_k = v[0]
                            if(RegData1==0):
                                RegData,RegData1=self.device.Data_to_be_written(RegData,dict_values_of_k)
                            else:
                                RegData,RegData1=self.device.Data_to_be_written(RegData1,dict_values_of_k)
                            lst+=RegData
                            if(dict_values_of_k["RegisterType"][0].lower()=="read"):
                                Logging.logger.warning("Input_value {} is Read Data type".format(input_values))
                            else:
                                data_check_status = self.device.DataCheckStatus(RegData, dict_values_of_k)
                                unitId, offset, length = self.device.Offset_Length_Unitid(self.device.getdevicesettings(),
                                                                                        dict_values_of_k)
                                
                                if (data_check_status == True):
                                    y=("".join(x for x in (re.findall("[a-zA-Z]",dict_values_of_k["DataType"][0]))).lower())
                                    if(y!="float"):
                                        write_result=Device_connection_master.write_registers(offset, 
                                            [(self.value_parsing.signed(RegData[register_number_value])) for register_number_value in range(len(dict_values_of_k["RegisterNumber"]))], unit=unitId)
                                        write_result_json['offset']=write_result
                                    else:
                                        var=[self.device.write_into_float(float(RegData[register_number_value])) if(("".join(x for x in (re.findall("[a-zA-Z]",dict_values_of_k["DataType"][register_number_value]))).lower())=="float") else self.value_parsing.signed(RegData[register_number_value]) for register_number_value in range(len(dict_values_of_k["RegisterNumber"]))]
                                        write_result=Device_connection_master.write_registers(offset, 
                                            var, unit=unitId,skip_encode=True)
                                        write_result_json['offset']=write_result
                                else:
                                    Logging.logger.warning("Can't Write Data into Register,Invalid Data")
                                    raise ValueError
                                break
            else:
                Logging.logger.exception(ConnectionError)
                raise ConnectionError
        except (ModbusIOException, error):
            write_result_json={"error Code":101,"Error Desc":"ModbusIOError"}
            Logging.logger.exception(error)
        except ParameterException as e:
            write_result_json={"error Code":102,"Error Desc":"Parameter Exception Error"}
            Logging.logger.exception(e)
        except ConnectionError as e:
            write_result_json={"error Code":103,"Error Desc":"Connection Error"}
            Logging.logger.exception(e)
        except AttributeError as e:
            write_result_json={"error Code":104,"Error Desc":"Attribute Error"}
            Logging.logger.exception(e)
        except TypeError as e:
            write_result_json={"error Code":105,"Error Desc":"Type Error"}
            Logging.logger.exception(e)
        except ValueError as e:
            write_result_json={"error Code":107,"Error Desc":"Value Error"}
            Logging.logger.exception(e)
        except Exception as e:
            write_result_json={"error Code":106,"Error Desc":"User Related Error"}
            Logging.logger.exception(e)
        finally:
            if(write_result==None):
                Logging.logger.info(write_result_json)
            else:
                if(dict_values_of_k["RegisterType"][0].lower()=="readwrite"):
                    if(write_result!=None):
                        response=self.modbus_block_read(input_List)
                        if(self.device.Response_validation(key_pair_values,response,lst, input_List)):
                            Logging.logger.info({"Read_Response":"Valid checking of Data of Read and Write"})
                        else:
                            Logging.logger.warning({"Read_Response":"Written Data does not match with Read data"})
                elif(dict_values_of_k["RegisterType"][0].lower()=="write"):
                    Logging.logger.info(write_result_json)
            Device_connection_master.close()
