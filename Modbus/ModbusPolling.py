from ModbusWrapper import Modbus
from time import sleep

def ModbusPollFunction(DeviceID,polling_frequecy):
    """ It prints Every information Related to DeviceID in Json Format

        :param: DeviceID and Polling_frequency 
        :return: Returns information related to Device id `ModbusPollFunction`
        :rtype: Json object
    """
    while True:
        input_list = ["UserDataBlock1","ReadWriteBlock1"] 
        # input_list = ["ReadWriteBlock1"]

        data = DeviceID.modbus_block_read(input_list)
        print("Modbus read data:", data)
        sleep(polling_frequecy)

DeviceID = Modbus("Sinexcel_batt_inv_01")
polling_frequecy = DeviceID.polling_freq()
ModbusPollFunction(DeviceID,polling_frequecy) 


'''
input_lst=["ReadWriteBlock1"]
for valuea in DataRan
    if(11<max and 11>min):
        data_typre(value):
        pass
regdata=[11,12,13] 
deviceId.ModbusBlock_write(regdata,input_lst)
'''

 
