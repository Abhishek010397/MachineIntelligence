from redistimeseries.client import Client
import datetime
import calendar
from flatten_json import flatten


class redis_storage:

   def __init__(self):
      self.rts = Client()

   def add_modbus_data(self, key, data, label):
      flat_json = flatten(data)
      current_datetime = datetime.datetime.utcnow()
      current_timetuple = current_datetime.utctimetuple()
      current_timestamp = calendar.timegm(current_timetuple)
      for k, v in flat_json.items():
         key_add = key+':'+k
         self.rts.add(key_add, current_timestamp, v, labels=label)

   def get_modbus_data(self, key, data):
      flat_json = flatten(data)
      for k, v in flat_json.items():
         key_add = key + ':' + k
         print(self.rts.get(key_add))

   def mget_modbus_data(self, value):
      print(self.rts.mget([value], with_labels=True))

   def info(self, data, key, label):
      flat_json = flatten(data)
      for k, v in flat_json.items():
         key_add = key+':'+k
         info = self.rts.info(key_add).__dict__
         print(info)


data = {'UserDataBlock1': {'Voltage': 29, 'Current': 209, 'Power': 3.0}}
c = redis_storage()
key = 'Sinexcel_batt_inv_01_1'
c.add_modbus_data(key, data, {'DeviceID': key})
c.get_modbus_data(key, data)
key_value = 'DeviceID='+key
c.mget_modbus_data(key_value)
c.info(data, key, {'DeviceID': key})
