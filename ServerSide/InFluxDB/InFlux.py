from influxdb import InfluxDBClient
import datetime
from Logger.LoggerHandling import Logging
from conf import influx_host,influx_port,mqttsub_json
import json

class InfluxDB:

    def __init__(self,dbname):
       
        host = influx_host
        port = influx_port
        self.dbname = dbname
        self.client = InfluxDBClient(host=host, port=port,database=dbname)

    def get_device_id(self):
        Logging.logger.info("{} function has been called".format("get_device_id()"))
        try:
            f = open(mqttsub_json, 'r')
            data = json.load(f)
            v1=0
            for key, value in data.items():
                if (key.lower() == "tags"):
                    for key, value in value.items():
                        if(key.lower()=="deviceid"):
                            v1=value
                    return(str(v1))
        except Exception as e:
            Logging.logger.exception({"error Code": 112, "Error Desc": e})
            Logging.logger.exception(e)

    def check_database(self,database):
        Logging.logger.info("{} function has been called".format("check_database()"))
        try:
            db_list = self.client.get_list_database()
            lst = []
            for json_data in db_list:
                for k, v in json_data.items():
                    lst.append(v)
            if (database in lst):
                Logging.logger.info("DATABASE EXISTS")
            else:
                Logging.logger.info("DATABASE NOT PRESENT, Creating The Database")
                self.client.create_database(dbname=database)
        except Exception as  e:
            Logging.logger.exception({"error Code": 112, "Error Desc": e})
            Logging.logger.error(e)

    def on_message_fetch(self, value,database):
        Logging.logger.info("{} function has been called".format("on_message_fetch()"))
        try:
            values = eval(value)
            d = {}
            for k, v in values.items():
                splitted_key = k.split(":")
                DeviceID_value = splitted_key[0]
                value_list = v[2]
                timestamp = v[1]
                for keys, values in v[0].items():
                    keys = keys
                    values = values

            field_value = (":".join(splitted_key))
            d[field_value] = eval(str(value_list))
            d[keys] = values

            d["timestamp"] = timestamp
            get_time = timestamp
            get_time = datetime.datetime.utcnow()
            form = get_time.isoformat("T") + "Z"
            device_id=self.get_device_id()
            json_body = [
                {
                    "measurement": "device_id",
                    "tags": {
                        keys: values
                    },
                    "time": form,
                    "fields": {
                        field_value: d[field_value]
                    }
                }
            ]
            self.check_database(database)
            self.client.write_points(json_body)
        except Exception as e:
            Logging.logger.exception({"error Code": 111, "Error Desc": e})
            Logging.logger.exception(e)

    def query_fetch(self):
        Logging.logger.info("{} function has been called".format("query_fetch()"))
        try:
            k = self.client.query('select * from Device2')
            print(k)
        except Exception as e:
            Logging.logger.exception({"error Code": 111, "Error Desc": e})
            Logging.logger.exception(e)
