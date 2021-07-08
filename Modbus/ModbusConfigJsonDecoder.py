import json

'''
Need to perform these functions
1.Device Setting Function ---> Input for this function is DeviceID, unique data to be returned
2.Device Info Function --> Input DeviceInfo String
3.User Data Block Function --> Input is User DataBlock String 
'''

class Modbusconfigjsondecoder:
    def __init__(self,DeviceID):
        self.DeviceID = DeviceID
    
    def getdevicesettings(self):
        try:
            f = open('modbus_config.json', 'r')
            data = json.load(f)
            for k, v in data.items():
                for k1,v1 in v.items():
                    if(k1 == "DeviceID" and v1 == self.DeviceID):
                        for k2,v2 in v.items():
                            if(k2 == "DeviceSettings"):
                                value = v2[0]
                                json_object = json.dumps(value, indent = 4)
                                return json_object

        except Exception as e:
            print(e)






        







