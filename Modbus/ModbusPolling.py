from Modbus.ModbusWrapper import Modbus
from Logger.LoggerHandling import Logging
import argparse

def ModbusPollFunction(DeviceID,list):
    """ It prints Every information Related to DeviceID in Json Format

        :param: DeviceID and Polling_frequency
        :return: Returns information related to Device id `ModbusPollFunction`
        :rtype: Json object
    """
    Logging.logger.info("You can Enter Input_List as per your preference")

    Logging.logger.info("Running Block_read")
    data = DeviceID.modbus_block_read(list)
    print(data)

def main():

    parser = argparse.ArgumentParser(prog='ModbusPolling', description='Modbus Polling Interface', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d', '--device_id', type=str,
                            help='Name Of Device', required=True)

    parser.add_argument('-l','--list', action='append', help='<Required> Set All Register Blocks', required=False)
    args = parser.parse_args()
    DeviceID =Modbus(args.device_id)
    ModbusPollFunction(DeviceID,args.list)

if __name__ == "__main__":
    main()




