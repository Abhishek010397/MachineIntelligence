""" Importing Modules """
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from struct import pack, unpack
import struct
import time
import logging
import json
import datetime as dt
from datetime import datetime
from dateutil import tz
import json

class Decoder:
    def __init__(self) -> None:
        pass

    def signed(self,value):
        packval = struct.pack('<h',value)
        return struct.unpack('<H',packval)[0]

    def s16(self,value):    
        return -(value & 0x8000) | (value & 0x7fff)

    def decode_32float(self,response):
        data = pack('>HH',response.registers[0], response.registers[1])
        return unpack('>f', data)[0]

    def decode_32int(self,response):
        retData = 0
        if len(response.registers) == 2:
            data = pack('>HH',response.registers[0], response.registers[1])
            retData = unpack('>i', data)[0]
        return retData

    def decode_64int(self,response):
        retData = 0
        if len(response.registers) == 4:
            data = pack('>HHHH', response.registers[0], response.registers[1], response.registers[2], response.registers[3])
            retData = unpack('>i', data)[0]
        return retData

    def fromRegisters(self,registers, byteorder):
        """ Initialize a payload decoder with the result of
        reading a collection of registers from a modbus device.
        The registers are treated as a list of 2 byte values.
        We have to do this because of how the data has already
        been decoded by the rest of the library.
        :param registers: The register results to initialize with
        :param endian: The endianess of the payload
        :returns: An initialized PayloadDecoder
        """
        if isinstance(registers, list):  # repack into flat binary
            payload = ''.join(pack('>H', x) for x in registers)
            return BinaryPayloadDecoder(payload, Endian)
            raise ParameterException('Invalid collection of registers supplied')


