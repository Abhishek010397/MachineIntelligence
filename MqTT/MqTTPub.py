import json
from Logger.LoggerHandling import Logging
from Redis_Storage.Time_Series import redis_storage
from paho.mqtt import client as mqtt_client
import argparse
from conf import broker, port, mqttpub_json


class MqttPub:

    def __init__(self,client_id):
        self.client = mqtt_client.Client(client_id)

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
        except Exception as e:
            print(e)
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
            print(e)
        finally:
            f.close()

    def on_connect(self, rc):
        try:
            Logging.logger.info("{} function has been called".format("mqtt_publish()"))
            if rc == 0:
                print("Connected to MQTT Broker!")
                return True
            else:
                print("Failed to connect, return code %d\n", rc)
                return False
        except Exception as e:
            Logging.logger.exception(e)

    def get_redis_data(self, value):
        try:
            Logging.logger.info("{} function has been called".format("get_redis_data()"))
            c = redis_storage()
            data = c.mget_modbus_data(value)
            Logging.logger.info(data)
            return data
        except Exception as e:
            Logging.logger.exception(e)

    def mqtt_publish(self, userdata):
        try:
            count = 0
            topic = self.json_variable_get()
            Logging.logger.info("{} function has been called".format("mqtt_publish()"))
            rc = self.client.connect(broker, port)
            flag = self.on_connect(rc)
            if flag == True:
                for i in userdata:
                    chunks = json.dumps(i)
                    result = self.client.publish(topic, chunks, qos=1)
                    count = count+1
                    Logging.logger.info(count)
                    status = result[0]
                    if status == 0:
                        print(f"Send `{chunks}` to topic `{topic}`")
                    else:
                        print(f"Failed to send message to topic {topic}")
            else:
                print(flag)
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
    k.mqtt_publish(data)



if __name__ == "__main__":
    main()

