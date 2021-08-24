from redistimeseries.client import Client
import datetime
import calendar
from flatten_json import flatten
import redis
from LoggerHandling import Logging

class redis_storage:

   def __init__(self):
      """
         This constructor calls the `Client()` Module to set the connection. 

         :raises redis.RedisError,redis.exceptions.ResponseError: when redis Module gives error, Exceptions will be raised
         :return: Connection Object
         :rtype: tuple
      """
      try:
         self.rts = Client()
      except redis.RedisError as e:
         Logging.logger.exception({"error Code":111,"Error Desc":e})
         Logging.logger.exception(e)
      except redis.exceptions.ResponseError as e:
         Logging.logger.exception({"error Code":112,"Error Desc":e})
         Logging.logger.exception(e)
         
   def add_modbus_data(self, key, data, label):
      """
         This function adds the fileds and values to the particular keys. 

         :param key, data, label: This function takes `key` , `data` and `label`
         :raises redis.RedisError,redis.exceptions.ResponseError: when redis Module gives error, Exceptions will be raised
         :return: add response
         :rtype: tuple
      """ 

      try:
         flat_json = flatten(data)
         current_datetime = datetime.datetime.utcnow()
         current_timetuple = current_datetime.utctimetuple()
         current_timestamp = calendar.timegm(current_timetuple)
         for k, v in flat_json.items():
            key_add = key+':'+k
            self.rts.add(key_add, current_timestamp, v, labels=label)
      except redis.RedisError as e:
         Logging.logger.exception({"error Code":111,"Error Desc":e})
         Logging.logger.exception(e)
      except redis.exceptions.ResponseError as e:
         Logging.logger.exception({"error Code":112,"Error Desc":e})
         Logging.logger.exception(e)

   def get_modbus_data(self, key, data):
      """
         This function gets the fileds and values that was added to the particular keys. 

         :param key, data: This function takes `key` and `data`
         :raises redis.RedisError,redis.exceptions.ResponseError: when redis Module gives error, Exceptions will be raised
         :return: get response
      """ 
      try:
         flat_json = flatten(data)
      except redis.RedisError as e:
         Logging.logger.exception({"error Code":111,"Error Desc":e})
         Logging.logger.exception(e)
      except redis.exceptions.ResponseError as e:
         Logging.logger.exception({"error Code":112,"Error Desc":e})
         Logging.logger.exception(e)
      finally:
         for k, v in flat_json.items():
            key_add = key + ':' + k
            Logging.logger.info(self.rts.get(key_add))

   def mget_modbus_data(self, value):
      """
         This function returns the `value`

         :param key, data: This function takes `value`
         :raises redis.RedisError,redis.exceptions.ResponseError: when redis Module gives error, Exceptions will be raised
         :return: get response
      """

      try:
         response=self.rts.mget([value], with_labels=True)
      except redis.RedisError as e:
         Logging.logger.exception({"error Code":111,"Error Desc":e})
         Logging.logger.exception(e)
      except redis.exceptions.ResponseError as e:
         Logging.logger.exception({"error Code":112,"Error Desc":e})
         Logging.logger.exception(e)
      finally:
         Logging.logger.info(response)

   def info(self, data, key, label):
      """
         This function returns the information related to keys

         :param key, data: This function takes `data` , `key` and `label`
         :raises redis.RedisError,redis.exceptions.ResponseError: when redis Module gives error, Exceptions will be raised
         :return: info response
      """

      try:
         flat_json = flatten(data)
      except redis.RedisError as e:
         Logging.logger.exception({"error Code":111,"Error Desc":e})
         Logging.logger.exception(e)
      except redis.exceptions.ResponseError as e:
         Logging.logger.exception({"error Code":112,"Error Desc":e})
         Logging.logger.exception(e)
      finally:
         for k, v in flat_json.items():
            key_add = key+':'+k
            response = self.rts.info(key_add).__dict__
            Logging.logger.info(response)


   
