from Modbus.ModbusWrapper import Modbus
from Logger.LoggerHandling import Logging
from Redis_Storage.Time_Series import redis_storage
from MqTT.MqTTPub import MqttPub


class ModbusPollFunction:

    def __init__(self,DeviceID):
        self.DeviceID = DeviceID

    def func(self):
        Logging.logger.info("Running Single_write")
        RegData = [1,2,3,4,5,-1]
        input_List = ["ReadWriteBlock1","ReadWriteBlock2","ReadWriteBlock3"]
        self.DeviceID.modbus_single_write(RegData, input_List)

        Logging.logger.info("Running Block_read")
        input_list_read = ["UserDataBlock1","ReadWriteBlock1","ReadWriteBlock2"]
        data = self.DeviceID.modbus_block_read(input_list_read)
        print(data)
        self.write_to_redis(data)

        Logging.logger.info("Running Block_write")
        RegData=[1,-3,1]
        input_List=["ReadWriteBlock2","ReadWriteBlock1"]
        self.DeviceID.modbus_block_write(RegData,input_List)

        Logging.logger.info("Running Block_read")
        input_list_read = ["UserDataBlock1","ReadWriteBlock1","ReadWriteBlock2"]
        data = self.DeviceID.modbus_block_read(input_list_read)
        print(data)
        self.write_to_redis(data)

    def write_to_redis(self,data):
        Logging.logger.info("{} function has been called".format("write_to_redis()"))
        c = redis_storage()
        key = 'Sinexcel_batt_inv_01'
        c.add_modbus_data(key, data, {'DeviceID': key})
        # key_value = 'DeviceID=' + key
        # self.call_mqtt(key_value)


    def call_mqtt(self,value):
        Logging.logger.info("{} function has been called".format("call_mqtt()"))
        client_id = "onslowBHP_BMS"
        k = MqttPub(client_id)
        k.get_redis_data(value)

DeviceID = Modbus("Sinexcel_batt_inv_01")
# polling_frequency = DeviceID.polling_freq()
m = ModbusPollFunction(DeviceID)
m.func()




