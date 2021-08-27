from Logger.LoggerHandling import Logging
from Redis_Storage.Time_Series import redis_storage

class MqttPub:

    def __init(self):
        pass

    def get_redis_data(self,value):
        try:
            Logging.logger.info("{} function has been called".format("get_redis_data()"))
            c = redis_storage()
            c.mget_modbus_data(value)
        except Exception as e:
             print(e)
