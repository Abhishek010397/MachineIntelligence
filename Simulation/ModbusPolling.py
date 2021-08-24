from Modbus.ModbusWrapper import Modbus
from time import sleep
from Logger.LoggerHandling import Logging
from Redis_Storage.Time_Series import redis_storage

def ModbusPollFunction(DeviceID):
    """ It prints Every information Related to DeviceID in Json Format

        :param: DeviceID and Polling_frequency
        :return: Returns information related to Device id `ModbusPollFunction`
        :rtype: Json object
    """
    Logging.logger.info("Running Single_write")
    RegData = [1,2,3,4,5,-1]
    input_List = ["ReadWriteBlock1","ReadWriteBlock2","ReadWriteBlock3"]
    DeviceID.modbus_single_write(RegData, input_List)

    Logging.logger.info("Running Block_read")    
    input_list_read = ["UserDataBlock1","ReadWriteBlock1","ReadWriteBlock2"]
    data = DeviceID.modbus_block_read(input_list_read)
    # print(data)

    c = redis_storage()
    key=str(DeviceID)
    c.add_modbus_data(key,data,{'DeviceID': key})
    c.get_modbus_data(key,data)
    key_value = 'DeviceID='+key
    c.mget_modbus_data(key_value)
    c.info(data, key, {'DeviceID': key})

    Logging.logger.info(data)

    Logging.logger.info("Running Block_write")
    RegData=[1,-3,1] 
    input_List=["ReadWriteBlock2","ReadWriteBlock1"] 
    DeviceID.modbus_block_write(RegData,input_List)
    
    Logging.logger.info("Running Block_read")    
    input_list_read = ["UserDataBlock1","ReadWriteBlock1","ReadWriteBlock2"]
    data = DeviceID.modbus_block_read(input_list_read)

    key=str(DeviceID)
    c.add_modbus_data(key,data,{'DeviceID': key})
    c.get_modbus_data(key,data)
    key_value = 'DeviceID='+key
    c.mget_modbus_data(key_value)
    c.info(data, key, {'DeviceID': key})

    Logging.logger.info(data)
    
    # sleep(polling_frequency)

DeviceID = Modbus("Sinexcel_batt_inv_01")
# polling_frequency = DeviceID.polling_freq()
ModbusPollFunction(DeviceID)



