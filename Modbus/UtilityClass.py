""" Importing Modules """
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from struct import pack, unpack
import struct
import time
import json
import datetime as dt
from datetime import datetime
from dateutil import tz
import json
from Logger.LoggerHandling import Logging

class Decoder:
    def __init__(self) -> None:
        pass

    def signed(self,value):
        """ This function takes value(positive or negative) as parameter 
        and returns the data by decoding it using signed()
        :param value: value is the data which has to be decoded using signed() function
        :returns: Decoded data
        """
        try:
            Logging.logger.info("{} function has been called".format("signed()"))
            packval = struct.pack('<h',value)
            data=struct.unpack('<H',packval)[0]
        except ValueError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return (data)

    def s16(self,value): 
        """ This function takes value as parameter 
        and returns the data by decoding it using s16()
        :param value: value is the data which has to be decoded using s16() function
        :returns: Decoded data
        """ 
        try:
            Logging.logger.info("{} function has been called".format("s16()")) 
            data=  -(value & 0x8000) | (value & 0x7fff) 
        except ValueError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return (data)

    def decode_32float(self,response):
        """ This function takes response value as parameter 
        and returns the data by decoding it using decode_32float()
        :param response: Response is the data which has to be decoded using decode_32float() function
        :returns: Decoded data
        """
        try:
            Logging.logger.info("{} function has been called".format("decode_32float()"))
            data = pack('>HH',response.registers[0], response.registers[1])
        except ValueError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return unpack('>f', data)[0]

    def decode_32int(self,response):
        """ This function takes response value as parameter 
        and returns the data by decoding it using decode_32int()
        :param response: Response is the data which has to be decoded using decode_32int() function
        :returns: Decoded data
        """
        try:
            Logging.logger.info("{} function has been called".format("decode_32int()"))
            retData = 0
            if len(response.registers) == 2:
                data = pack('>HH',response.registers[0], response.registers[1])
                retData = unpack('>i', data)[0]
            return retData
        except ValueError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return retData

    def decode_64int(self,response):
        """ This function takes response value as parameter 
        and returns the data by decoding it using decode_64int()
        :param response: Response is the data which has to be decoded using decode_64int() function
        :returns: Decoded data
        """
        try:
            Logging.logger.info("{} function has been called".format("decode_64int()"))
            retData = 0
            if len(response.registers) == 4:
                data = pack('>HHHH', response.registers[0], response.registers[1], response.registers[2], response.registers[3])
                retData = unpack('>i', data)[0]
        except ValueError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return retData
    
    def string16(self,value):
        count = 4 #Read 4 16bit registers
    
        result = client.read_holding_registers(25000,count)
        
        for i in range(count):
            result.registers[i] = struct.unpack("<H", struct.pack(">H", result.registers[i]))[0]
        
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers)

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
        try:
            Logging.logger.info("{} function has been called".format("fromRegisters()"))
            if isinstance(registers, list): 
                payload = ''.join(pack('>H', x) for x in registers)
                raise ValueError('Invalid collection of registers supplied')
        except ValueError as e:
            Logging.logger.exception(e)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            return BinaryPayloadDecoder(payload, Endian)



