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
Defining Block_write() function
'''
def Block_write(setReg): 
    TCPmaster2 = ModbusClient("127.0.0.1", port=502) 
    pvInvConn = TCPmaster2.connect()

    if (pvInvConn is True):
        res = TCPmaster2.write_registers(30001, setReg, unit=1)
    TCPmaster2.close()
'''
Manuallly Writting into Register
'''
setReg=[100,111,97] 
Block_write(setReg)
