from ModbusWrapper import Modbus
from time import sleep
from LoggerHandling import Logging

def ModbusPollFunction(DeviceID, polling_frequecy):
    """ It prints Every information Related to DeviceID in Json Format

        :param: DeviceID and Polling_frequency
        :return: Returns information related to Device id `ModbusPollFunction`
        :rtype: Json object
    """
    for iteartion_limit in range(3):
        input_list = ["UserDataBlock1"]
        data = DeviceID.modbus_block_read(input_list)
        Logging.logger.info('Modbus read data: %s', data)
        sleep(polling_frequecy)
        RegData = [2, 2, 2, 2, 2, 2]
        input_List = ["ReadWriteBlock1", "ReadWriteBlock2"]
        DeviceID.modbus_single_write(RegData, input_List)


DeviceID = Modbus("Sinexcel_batt_inv_01")
polling_frequecy = DeviceID.polling_freq()
ModbusPollFunction(DeviceID, polling_frequecy)

