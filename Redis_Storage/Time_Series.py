from redistimeseries.client import Client
import datetime
import calendar


class redis_storage:

   def __init__(self,key,data):
      self.key = key
      self.data =  data
      self.rts = Client()
      self.create()
      self.add()
      self.get()

   def create(self):
      self.rts.create(self.key, labels={'Time':'Series'})

   def add(self):
      current_datetime = datetime.datetime.utcnow()
      current_timetuple = current_datetime.utctimetuple()
      current_timestamp = calendar.timegm(current_timetuple)
      self.rts.add(self.key, current_timestamp, 5.1 )

   def get(self):
      print(self.rts.get(self.key))

data = 'ReadWriteBlock1'
c = redis_storage('Sinexcel_batt_inv_01', data)
'''       
rts = Client()
rts.create('test2', labels={'Time':'Series'})
#rts.add('test1', 1, 1.12)
#rts.add('test1', 2, 1.12)
#rts.incrby('test',1.2)
#rts.incrby('test1',1)
print(rts.get('test2'))
#print(rts.get('test1'))
#rts.incrby('test1',1)
#rts.range('test1', 0, -1)
#rts.range('test1', 0, -1, aggregation_type='avg', bucket_size_msec=10)
#rts.range('test1', 0, -1, aggregation_type='sum', bucket_size_msec=10)
#rts.info('test1').__dict__
# Example with rules
rts.create('source', retention_msecs=40)
rts.create('sumRule')
rts.create('avgRule')
rts.createrule('source', 'sumRule', 'sum', 20)
rts.createrule('source', 'avgRule', 'avg', 15)
rts.add('source', '*', 1)
rts.add('source', '*', 2)
rts.add('source', '*', 3)
rts.get('sumRule')
rts.get('avgRule')
rts.info('sumRule').__dict__
'''