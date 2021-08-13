from redistimeseries.client import Client
import datetime
import calendar
from flatten_json import flatten

class redis_storage:

   def __init__(self):
      self.rts = Client()

   def create_modbus_key(self,key_add):
      self.rts.create(key_add)
      key_add = None

   def add_modbus_data(self,key,data):
      flat_json=flatten(data)
      current_datetime = datetime.datetime.utcnow()
      current_timetuple = current_datetime.utctimetuple()
      current_timestamp = calendar.timegm(current_timetuple)
      for k,v in flat_json.items():
         key_add=key+':'+k
         create_key=self.create_modbus_key(key_add)
         self.rts.add(key_add,current_timestamp, v)

   def get_modbus_data(self,key,data):
      flat_json=flatten(data)
      for k,v in flat_json.items():
         key_add = key + ':' + k
         print(self.rts.get(key_add))

data = {'UserDataBlock1': {'Voltage': 14, 'Current': 114, 'Power': 1.5}}
c = redis_storage()
key='Sinexcel_batt_inv_01'
c.add_modbus_data(key,data)
c.get_modbus_data(key,data)

