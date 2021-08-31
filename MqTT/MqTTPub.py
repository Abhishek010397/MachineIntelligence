from Logger.LoggerHandling import Logging
from Redis_Storage.Time_Series import redis_storage
import paho.mqtt.client as mqtt
import time

Connected = False


class MqttPub:

    def __init(self, addr, port, clientId):
        self.address = addr
        self.port = port
        self.client_id = clientId
        self.client = mqtt.Client(clientId, clean_session=True)

    def on_connect(self, rc):
        try:
            if rc == 0:
                global Connected
                Connected = True
            else:
                print("False")
        except Exception as e:
            print(e)

    def get_redis_data(self, value):
        try:
            Logging.logger.info(
                "{} function has been called".format("get_redis_data()"))
            c = redis_storage()
            data = c.mget_modbus_data(value)
            Logging.logger.info(data)
            Connection = self.on_connect()
            if (Connection == True):
                self.mqtt_publish(data)
            else:
                time.sleep(0.01)
        except Exception as e:
            Logging.logger.exception(e)

    def mqtt_publish(self, client, userdata, mid):
        try:
            Logging.logger.info(
                "{} function has been called".format("mqtt_publish()"))
            self.client.connect("localhost", 1883, 60)
            self.client.publish("onslowBHP_BMS/BatteryData", userdata, qos=1)
        except Exception as e:
            Logging.logger.exception(e)
        finally:
            self.client.disconnect()
