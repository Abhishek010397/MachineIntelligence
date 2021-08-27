from redistimeseries.client import Client
import datetime
import calendar
from flatten_json import flatten
import redis
from Logger.LoggerHandling import Logging

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
         count = 0
         Logging.logger.info("{} function has been called".format("add_modbus_data()"))
         flat_json = flatten(data)
         current_datetime = datetime.datetime.utcnow()
         current_timetuple = current_datetime.utctimetuple()
         current_timestamp = calendar.timegm(current_timetuple)
         for k, v in flat_json.items():
            count = count+1
            print(count)
            key_add = key + ':' + k
            self.rts.add(key_add, current_timestamp, v, labels=label)
      except Exception as e:
         Logging.logger.exception(e)

      # except redis.RedisError as e:
      #    Logging.logger.exception({"error Code":111,"Error Desc":e})
      #    Logging.logger.exception(e)


   def get_modbus_data(self, key, data):
      """
         This function gets the fileds and values that was added to the particular keys. 

         :param key, data: This function takes `key` and `data`
         :raises redis.RedisError,redis.exceptions.ResponseError: when redis Module gives error, Exceptions will be raised
         :return: get response
      """ 
      try:
         Logging.logger.info("{} function has been called".format("get_modbus_data()"))
         flat_json = flatten(data)
         for k, v in flat_json.items():
            key_add = key + ':' + k
            print(key_add)
            response = self.rts.get(key_add)
            Logging.logger.info(response)
      except redis.RedisError as e:
         Logging.logger.exception({"error Code":111,"Error Desc":e})
         Logging.logger.exception(e)
      except redis.exceptions.ResponseError as e:
         Logging.logger.exception({"error Code":112,"Error Desc":e})
         Logging.logger.exception(e)
      finally:
         return response


   def mget_modbus_data(self, value):
      """
         This function returns the `value`

         :param key, data: This function takes `value`
         :raises redis.RedisError,redis.exceptions.ResponseError: when redis Module gives error, Exceptions will be raised
         :return: get response
      """

      try:
         Logging.logger.info("{} function has been called".format("mget_modbus_data()"))
         response=self.rts.mget([value], with_labels=True)
         # Logging.logger.info(response)
      except redis.RedisError as e:
         Logging.logger.exception({"error Code":111,"Error Desc":e})
         Logging.logger.exception(e)
      except redis.exceptions.ResponseError as e:
         Logging.logger.exception({"error Code":112,"Error Desc":e})
         Logging.logger.exception(e)
      finally:
         return response

   def info(self, data, key, label):
      """
         This function returns the information related to keys

         :param key, data: This function takes `data` , `key` and `label`
         :raises redis.RedisError,redis.exceptions.ResponseError: when redis Module gives error, Exceptions will be raised
         :return: info response
      """

      try:
         Logging.logger.info("{} function has been called".format("info()"))
         flat_json = flatten(data)
         for k, v in flat_json.items():
            key_add = key+':'+k
            response = self.rts.info(key_add).__dict__
            Logging.logger.info(response)
      except redis.RedisError as e:
         Logging.logger.exception({"error Code":111,"Error Desc":e})
         Logging.logger.exception(e)
      except redis.exceptions.ResponseError as e:
         Logging.logger.exception({"error Code":112,"Error Desc":e})
         Logging.logger.exception(e)
      finally:
         return response


