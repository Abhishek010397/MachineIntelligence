from ModbusWrapper import Modbus
from time import sleep

sinexcel_batt_inv_01 = Modbus("Sinexcel_batt_inv_01")

polling_frequecy = sinexcel_batt_inv_01.polling_freq()

while True:

    input_list = ["DeviceInfoBlock", "UserDataBlock1"]
    data = sinexcel_batt_inv_01.modbus_block_read(input_list)
    print("Modbus read data:", data)

    '''TODO:Send it to redis db'''

    sleep(polling_frequecy)


 
