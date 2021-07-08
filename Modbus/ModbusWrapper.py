'''
import sys
import traceback
from struct import pack, unpack, error
from time import sleep
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ModbusIOException, ParameterException, ConnectionException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pytz import timezone
import struct

'''
from ModbusConfigJsonDecoder import Modbusconfigjsondecoder

class Modbus:
    def __init__(self, param):
        device = Modbusconfigjsondecoder(param)
        #device_setting = []
        device_setting = [device.getdevicesettings()]
        print(device_setting)
        self.response = param
'''Get Json Objects Filtered Out Here

    def modbus_block_read(self, device_setting, input_list):
        try:
            DEVICE_CONNECTION = device_setting.connect()
            if (DEVICE_CONNECTION == True):
                
                call pymodbus read register_function(input_list_decoded)
                
        except Exception as e:
            print(e)

    def modbus_single_write(self):
        return 

    def modbus_block_write(self):
        return 
'''
