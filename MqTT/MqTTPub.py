import json
import time
from Logger.LoggerHandling import Logging
from Redis_Storage.Time_Series import redis_storage
from paho.mqtt import client as mqtt_client
import argparse
from conf import broker, port,mqttpub_json

class MqttPub:

    def __init__(self,client_id):
        self.client = mqtt_client.Client(client_id,clean_session=True)

    def get_json_key_variable(self,client_id):
        try:
            f = open(mqttpub_json, 'r')
            data = json.load(f)
            for key, value in data.items():
                if (key.lower() == "clientid" and client_id == value):
                    for key, value in data.items():
                        if (key.lower() == "tags"):
                            for key, value in value.items():
                                if (key.lower() == "deviceid"):
                                    k = 'DeviceID='+value
                                    return k
                else:
                    Logging.logger.error("ClientID IS NOT PRESENT")
                    exit()
        except Exception as e:
            Logging.logger.exception({"error Code": 111, "Error Desc": e})
            Logging.logger.exception(e)
        finally:
            f.close()

    def json_variable_get(self):
        try:
            f = open(mqttpub_json, 'r')
            data = json.load(f)
            for key, value in data.items():
                if (key.lower() == "tags"):
                    for key, value in value.items():
                        if (key.lower() == "topic"):
                            return value
        except Exception as e:
            Logging.logger.exception({"error Code": 112, "Error Desc": e})
            Logging.logger.exception(e)
        finally:
            f.close()

    def on_connect(self, rc):
        try:
            Logging.logger.info("{} function has been called".format("on_connect()"))
            if rc == 0:
                Logging.logger.info("Connected to MQTT Broker!")
                return True
            else:
                Logging.logger.info("Failed to connect, return code %d\n", rc)
                return False
        except Exception as e:
            Logging.logger.exception(e)

    def get_redis_data(self, value):
        try:
            Logging.logger.info("{} function has been called".format("get_redis_data()"))
            c = redis_storage()
            data = c.mget_modbus_data(value)
            if(bool(data)==False):
                Logging.logger.error({"****UNABLE TO RETRIEVE DATA FROM REDISTIMESERIES DATABASE****"})
                Logging.logger.error({"PLEASE VERIFY IF DATA IS BEING WRITTEN IN REDISTIMESERIES!"})
                exit()
            else:    
                Logging.logger.info(data)
                return data
        except Exception as e:
            Logging.logger.exception(e)

    def split_data(self,data):
        try:
            Logging.logger.info("{} function has been called".format("split_data()"))
            count = 0
            for i in data:
                chunks = json.dumps(i)
                count = count + 1
                Logging.logger.info('{0} COUNTER VALUE'.format(count))
                self.mqtt_publish(chunks)
        except Exception as e:
            Logging.logger.exception(e)

    def mqtt_publish(self, userdata):
        try:
            Logging.logger.info("{} function has been called".format("mqtt_publish()"))
            topic = self.json_variable_get()
            rc = self.client.connect(broker,port)
            flag = self.on_connect(rc)
            if flag == True:
                result = self.client.publish(topic, userdata, retain=True,qos=0)
                status = result[0]
                if status == 0:
                    print(f"Send `{userdata}` to topic `{topic}`")
                    time.sleep(5)
                else:
                    print(f"Failed to send message to topic {topic}")
            else:
                Logging.logger.info("CONNECTION ERROR")
        except Exception as e:
            Logging.logger.exception(e)

def main():
    parser = argparse.ArgumentParser(prog='MqTTPub', description='MqTTPub interface',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--client_id', type=str, help='Name of client id', required=True)

    args = parser.parse_args()
    k = MqttPub(args.client_id)
    value = k.get_json_key_variable(args.client_id)
    data = k.get_redis_data(value)
    k.split_data(data)

if __name__ == "__main__":
    main()

