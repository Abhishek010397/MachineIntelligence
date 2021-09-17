from influxdb import InfluxDBClient
import datetime
from Logger.LoggerHandling import Logging

class InfluxDB:

    def __init__(self,dbname):

        host = 'host'
        port = 8086
        self.dbname = dbname
        self.client = InfluxDBClient(host=host, port=port,database=dbname)

    def on_message_fetch(self, value,dbname):
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
            json_body = [
                {
                    "measurement": "Device2",
                    "tags": {
                        keys: values
                    },
                    "time": form,
                    "fields": {
                        field_value: d[field_value]
                    }
                }
            ]
            self.client.create_database(dbname=dbname)
            self.client.write_points(json_body)
        except Exception as e:
            Logging.logger.exception({"error Code": 111, "Error Desc": e})
            Logging.logger.exception(e)

    def query_fetch(self):
        Logging.logger.info("{} function has been called".format("query_fetch()"))
        try:
            k = self.client.query('select * from Device2')
            print("influx response", k)
        except Exception as e:
            Logging.logger.exception({"error Code": 111, "Error Desc": e})
            Logging.logger.exception(e)







