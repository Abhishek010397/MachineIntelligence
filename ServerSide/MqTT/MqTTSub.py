import paho.mqtt.client as mqtt
import argparse
from conf import broker, port, mqttsub_json
import json
from Logger.LoggerHandling import Logging
from InFluxDB.InFlux import InfluxDB

class MqTTSub:

    def __init__(self, clientid):
        self.client = mqtt.Client(clientid)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        Logging.logger.info("Connecting To MqTT Broker")
        self.client.connect(broker, port)
        self.client.loop_forever()

    def get_json_key_variable(clientid):
        Logging.logger.info("{} function has been called".format("get_json_key_variable()"))
        try:
            f = open(mqttsub_json, 'r')
            data = json.load(f)
            for key, value in data.items():
                if (key.lower() == "clientid" and clientid == value):
                    return value
                else:
                    Logging.logger.error("ClientID IS NOT PRESENT")
                    exit()
        except Exception as e:
            Logging.logger.exception({"error Code": 111, "Error Desc": e})
            Logging.logger.exception(e)
        finally:
            f.close()

    def json_variable_get(self):
        Logging.logger.info("{} function has been called".format("json_variable_get()"))
        try:
            f = open(mqttsub_json, 'r')
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

    def get_dbname(self):
        Logging.logger.info("{} function has been called".format("get_dbname()"))
        try:
            f = open(mqttsub_json, 'r')
            data = json.load(f)
            for key, value in data.items():
                if (key.lower() == "tags"):
                    for key, value in value.items():
                        if (key.lower() == "dbname"):
                            return value
        except Exception as e:
            Logging.logger.exception({"error Code": 112, "Error Desc": e})
            Logging.logger.exception(e)
        finally:
            f.close()

    def on_message(self, client, userdata, message):
        Logging.logger.info("{} function has been called".format("on_message()"))
        Message=str(message.payload.decode("utf-8"))
        Topic = str(message.topic)
        Logging.logger.info('Message %s Recieved From Topic %s' % (Message,Topic))
        if message.retain == 1:
            Logging.logger.info("Message Retained")
            dbname=self.get_dbname()
            c=InfluxDB(dbname)
            c.on_message_fetch(Message,dbname)
        else:
            Logging.logger.error("Message Not Retained")

    def on_connect(self, client, userdata, flags, rc):
        Logging.logger.info("{} function has been called".format("on_connect()"))
        if rc == 0:
            Logging.logger.info("{} Connection OK, Returned code".format(rc))
            Logging.logger.info("Subscribing to topic")
            topic = self.json_variable_get()
            client.subscribe(topic,qos=0)
        else:
            Logging.logger.error("{} Bad Connection Error".format(rc))

def main():
    parser = argparse.ArgumentParser(prog='MqTTSub', description='MqTTSub interface',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--client_id', type=str, help='Name of client id', required=True)
    args = parser.parse_args()
    value = MqTTSub.get_json_key_variable(args.client_id)
    MqTTSub(value)

if __name__ == "__main__":
    main()
