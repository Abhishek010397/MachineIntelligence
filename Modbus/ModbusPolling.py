from Modbus.ModbusWrapper import Modbus
from Logger.LoggerHandling import Logging
import argparse
from Redis_Storage.Time_Series import redis_storage


class ModbusPolling:

    def __init__(self,DeviceID,list,deviceid_argument):
        self.DeviceID=DeviceID
        self.list=list
        self.deviceid_argument=deviceid_argument

    def ModbusPollFunction(self):

        """ It prints Every information Related to DeviceID in Json Format

            :param: DeviceID and Polling_frequency
            :return: Returns information related to Device id `ModbusPollFunction`
            :rtype: Json object
        """
        Logging.logger.info("You can Enter Input_List as per your preference")

        Logging.logger.info("Running Block_read")
        data = self.DeviceID.modbus_block_read(self.list)
        # print("modbus_block_read",data)

        self.write_to_redis(data)

    def write_to_redis(self,data):
        Logging.logger.info("{} function has been called".format("write_to_redis()"))
        if((self.list)==None):
            Logging.logger.error("***Can't write into redis , None data***")
            exit()
        c = redis_storage()
        key=str(self.deviceid_argument)
        c.add_modbus_data(key, data, {'DeviceID': key})

def main():

    parser = argparse.ArgumentParser(prog='ModbusPolling', description='Modbus Polling Interface', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d', '--device_id', type=str,
                            help='Name Of Device', required=True)

    parser.add_argument('-l','--list', action='append', help='<Required> Set All Register Blocks', required=False)
    args = parser.parse_args()
    deviceid_argument=args.device_id
    DeviceID =Modbus(deviceid_argument)
    obj=ModbusPolling(DeviceID,args.list,deviceid_argument)
    obj.ModbusPollFunction()

if __name__ == "__main__":
    main()




