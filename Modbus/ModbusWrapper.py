import sys
import traceback
from time import sleep
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ModbusIOException, ParameterException, ConnectionException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pytz import timezone
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRTU

from ModbusConfigJsonDecoder import Modbusconfigjsondecoder
from UtilityClass import Decoder


class Modbus:
    def __init__(self, DeviceID):

        self.device = Modbusconfigjsondecoder(DeviceID)
        self.device_setting = self.device.getdevicesettings()
        self.DeviceInfoBlock = self.device.getdeviceinfo()
        self.UserDataBlock1 = self.device.userdatablock()
        self.response = DeviceID

    def polling_freq(self):
        poll_frequency = self.device.Get_polling_freq()
        return(poll_frequency)

    def connect_function(self):
        try:
            connect_type = self.device.ConnectionType()
            if(connect_type == "TCP"):
                IPAddress_value, Port_value = self.device.Tcp_function(
                    self.device_setting)
                Device_connection_master = ModbusClient(
                    IPAddress_value, int(Port_value))
                device_connector = Device_connection_master.connect()
                return (Device_connection_master, device_connector)

            elif(connect_type == "RTU"):
                Device_connection_master = self.device.RTU_function(
                    self.device_setting)
                device_connector = Device_connection_master.connect()
                return (Device_connection_master, device_connector)
        except Exception as e:
            print(e)

    def modbus_block_read(self, input_list):
        Device_connection_master, device_connector = self.connect_function()
        try:
            if(device_connector == True):
                for input_values in input_list:
                    if(input_values == "DeviceInfoBlock"):
                        unitId, offset, length = self.device.Offset_Length_Unitid(
                            self.device_setting, self.DeviceInfoBlock)
                        response = Device_connection_master.read_holding_registers(
                            offset, length, unit=unitId)
                        decoder = BinaryPayloadDecoder.fromRegisters(
                            response.registers, byteorder=Endian.Big)
                        Device_connection_master.close()
                    elif(input_values == "UserDataBlock1"):
                        pass
                    elif(input_values == "DeviceName"):
                        return (str(self.device.getdevicename()))
                    elif(input_values == "ConnType"):
                        return (str(self.device.ConnectionType()))
        except (ModbusIOException, ParameterException, ConnectionException, error):
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            Device_connection_master.close()
            return
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            sleep(30)
            Device_connection_master.close()
            return
        else:
            Device_connection_master.close()
            ''' return (look at word document)'''

    def modbus_single_write(self):
        return

    def modbus_block_write(self):
        return




