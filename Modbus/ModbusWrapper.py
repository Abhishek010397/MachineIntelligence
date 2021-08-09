import sys
import traceback
from struct import pack, unpack, error
from time import sleep
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ModbusIOException, ParameterException, ConnectionException
from pymodbus.payload import BinaryPayloadDecoder
import json
from pymodbus.constants import Endian
from ModbusConfigJsonDecoder import Modbusconfigjsondecoder
from LoggerHandling import Logging


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
        self.device = Modbusconfigjsondecoder(DeviceID)
        self.device_setting = self.device.getdevicesettings()
        # self.DeviceInfoBlock= self.device.getdeviceinfo()
        # self.UserDataBlock1=  self.device.userdatablock()

    def polling_freq(self):
        """ This function calls the Get_polling_freq() function defined in Modbusconfigjsondecoder Module to get the poll_frequency

        :return: poll_frequency for each deviceID
        :rtype: int

        """
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
            connect_type = self.device.ConnectionType()
            if (connect_type == "TCP"):

                IPAddress_value, Port_value = self.device.Tcp_function(self.device_setting)
                Device_connection_master = ModbusClient(IPAddress_value, int(Port_value))
                device_connector = Device_connection_master.connect()
                return (Device_connection_master, device_connector)
            elif (connect_type == "RTU"):

                Device_connection_master = self.device.RTU_function(self.device_setting)
                device_connector = Device_connection_master.connect()
                return (Device_connection_master, device_connector)
        except Exception as e:
            print(e)

    def modbus_block_read(self, input_list):
        """
            This function returns every values what we write into `register`. it gets the values values from connect_function() and checks if Connection is `True`. It iterates through input_list and accordingly returns Values in Json format via functions defined in ModbusConfigJsonDecoder Module

            :param modbus_block_read: input_list passed from ModbusPolling Module
            :raises ModbusIOException,ParameterException,ConnectionException: when either of the Exceptions occur, it will taise Errors
            :return: Json object
            :rtype: json
        """

        Device_connection_master, device_connector = self.connect_function()
        '''
        Checking if My Connection has Connected to Server 
        '''
        print(Device_connection_master, device_connector)

        final_json_data = {}
        try:
            if (device_connector == True):
                '''
                Iterating through input_list to return data Accordingly
                '''
                key_pair_values = self.device.keys_get_function()
                for input_values in input_list:
                    nested_json_data = {}
                    for k, v in key_pair_values.items():
                        if (input_values == k):
                            dict_values_of_k = v[0]
                            # print(dict_values_of_k)
                            unitId, offset, length = self.device.Offset_Length_Unitid(self.device_setting,
                                                                                      dict_values_of_k)
                            print(unitId, offset, length)
                            response = Device_connection_master.read_holding_registers(offset, length, unit=unitId)
                            decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Big)

                            for RegisterName_indexing in range(len(dict_values_of_k["RegisterName"])):

                                datatype_response = self.device.dataTypeResponse(decoder, dict_values_of_k["DataType"][
                                    RegisterName_indexing])
                                """
                                Checking Validation of Data 
                                """
                                data_response_validation = self.device.DataResponseValidation(datatype_response,
                                                                                              RegisterName_indexing,
                                                                                              dict_values_of_k)
                                if (data_response_validation == True):
                                    """
                                    Multiplying the Actual Data with Multiplier
                                    """
                                    nested_json_data[
                                        str(dict_values_of_k["RegisterName"][RegisterName_indexing])] = round(
                                        datatype_response * (
                                            eval(dict_values_of_k["Multiplier"][RegisterName_indexing])), 3)

                            final_json_data[str(input_values)] = dict(nested_json_data)
                            del nested_json_data

        except (ModbusIOException, error):
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        except ParameterException as e:
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        except ConnectionException as e:
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        finally:
            Device_connection_master.close()
            return (final_json_data)

    def modbus_single_write(self, RegData, input_List):

        # if(resgister_type=="read"):
        #     return ('DataType is Read')

        """
            It will write into Register one by one via Iteration

            :param modbus_single_write: RegisterData and input_List
        """
        Device_connection_master, device_connector = self.connect_function()
        try:
            if (device_connector == True):
                key_pair_values = self.device.keys_get_function()
                for input_values in input_List:
                    for k, v in key_pair_values.items():
                        if (input_values == k):
                            dict_values_of_k = v[0]
                            unitId = self.device.Unitid_singleWrite(self.device_setting, dict_values_of_k)
                            data_check_status = self.device.DataCheckStatus(RegData, dict_values_of_k)
                            if (data_check_status == True):
                                for register_number_value in range(len(dict_values_of_k["RegisterNumber"])):
                                    write_result = Device_connection_master.write_registers(
                                        int(dict_values_of_k["RegisterNumber"][register_number_value]),
                                        int(RegData[register_number_value]), unit=unitId)

                                    ''' it will return write_result...boolean value '''

                            else:
                                print("Data Incorrect!!")

        except (ModbusIOException, error):
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        except ParameterException as e:
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        except ConnectionException as e:
            traceback.print_exc(file=sys.stdout)
            # sleep(30)
            return
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            # sleep(30)
            return
        finally:
            # if(registerType=="readwrite"):
            #     if(write_result==True):
            #         print(self.modbus_block_read(input_List))
            #     else:
            #         return (write_result)
            # elif(registerType=="write"):
            #     return (write_result)

            Device_connection_master.close()
            # return(res)

    def modbus_block_write(self, RegData, input_List):

        """
            It will write into Register block wise without Iterating

            :param modbus_block_write: RegisterData and input_List
        """

        Device_connection_master, device_connector = self.connect_function()
        try:
            if (device_connector == True):
                key_pair_values = self.device.keys_get_function()
                for input_values in input_List:
                    for k, v in key_pair_values.items():
                        if (input_values == k):
                            dict_values_of_k = v[0]
                            data_check_status = self.device.DataCheckStatus(RegData, dict_values_of_k)
                            unitId, offset, length = self.device.Offset_Length_Unitid(self.device_setting,
                                                                                      dict_values_of_k)
                            if (data_check_status == True):
                                Device_connection_master.write_registers(offset, RegData, unit=unitId)
                            else:
                                print("Can't Write Data into Register,Invalid Data")
                            break
        except (ModbusIOException, error):
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        except ParameterException as e:
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        except ConnectionException as e:
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            return
        finally:
            print(self.modbus_block_read(input_List))
            Device_connection_master.close()




        

