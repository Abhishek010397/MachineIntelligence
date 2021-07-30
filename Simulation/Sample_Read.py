'''
Importing The Modules
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
import json
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRTU

'''
Defining Block_read() function to check the Data 
'''
def Block_read(): 

    TCPmaster2 = ModbusClient("127.0.0.1", port=502)  
    pvInvConn = TCPmaster2.connect()
    if (pvInvConn is True):
        res = TCPmaster2.read_holding_registers(768, 3, unit=1)
        decoder = BinaryPayloadDecoder.fromRegisters(res.registers, byteorder=Endian.Big)
        x1=decoder.decode_16bit_int()
        x2=decoder.decode_16bit_int()
        x3=decoder.decode_16bit_int()
        print(x1,x2,x3,sep=" ")

    TCPmaster2.close()

'''
Calling The Function
'''
Block_read()