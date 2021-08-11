from ModbusWrapper import Modbus
from time import sleep
from LoggerHandling import Logging
from Redis_Storage.Time_Series import redis_storage

def ModbusPollFunction(DeviceID, polling_frequency):
    """ It prints Every information Related to DeviceID in Json Format

        :param: DeviceID and Polling_frequency
        :return: Returns information related to Device id `ModbusPollFunction`
        :rtype: Json object
    """
    RegData = [-6,6,3,-1,2,3]
    input_List = ["ReadWriteBlock1","ReadWriteBlock2"]
    DeviceID.modbus_single_write(RegData, input_List)
    Logging.logger.info("Running Block_write")
        

    # input_list_read = ["UserDataBlock1","ReadWriteBlock1","ReadWriteBlock2"]
    # data = DeviceID.modbus_block_read(input_list_read)
    # Logging.logger.info('Modbus read data: %s', data)

    RegData=[-3,-7,3,2,-8,4] 
    input_List=["UserDataBlock1","ReadWriteBlock1","ReadWriteBlock2"] 
    DeviceID.modbus_block_write(RegData,input_List)

    # input_list_read = ["UserDataBlock1","ReadWriteBlock1","ReadWriteBlock2"]
    # data = DeviceID.modbus_block_read(input_list)
    # Logging.logger.info('Modbus read data: %s', data)

    #sleep(polling_frequency)

DeviceID = Modbus("Sinexcel_batt_inv_01")
polling_frequency = DeviceID.polling_freq()
ModbusPollFunction(DeviceID, polling_frequency)



