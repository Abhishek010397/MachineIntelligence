import json
import argparse
import datetime
import time
from redistimeseries.client import Client
import redis

flag = 0
class Alerts:

    def __init__(self, priority_val):
        self.priority = priority_val

    def getKeysOperation(self):
        try:
            f = open('user-alerts.json', 'r')
            data = json.load(f)
            for key, value in data.items():
                for key1, value1 in value.items():
                    if (key1 == 'Priority' and value1 == int(self.priority)):
                        for key2, value2 in value.items():
                            if key2 == 'RegistersKey':
                                matches = [match for match in value2]
                                RtsKeys = '%s' % ','.join(matches)
                            if key2 == 'Threshold':
                                matches = [match for match in value2]
                                ThresholdKeys = '%s' % ','.join(matches)
                            if key2 == 'Operator':
                                matches = [match for match in value2]
                                OperatorKeys = '%s' % ','.join(matches)
                            if key2 == 'Operator1':
                                matches = [match for match in value2]
                                Operator1Keys = '%s' % ','.join(matches)
                            if key2 == 'Result':
                                matches = [match for match in value2]
                                ResultKeys = '%s' % ','.join(matches)
                            if key2 == 'TimeRange':
                                matches = [match for match in value2]
                                Time = '%s' % ','.join(matches)
                        return RtsKeys, ThresholdKeys, OperatorKeys, Operator1Keys, ResultKeys, Time
        except Exception as e:
            print(e)

    def compareOperations(self, key, threshold, operator):
        try:
            res = []
            for i in range(len(key)):
                if str(operator[i]) == ">":
                    if int(key[i]) > int(threshold[i]):
                        result = 1
                        res.append(result)
                    else:
                        result = 0
                        res.append(result)
                if str(operator[i]) == "<":
                    if int(key[i]) < int(threshold[i]):
                        result = 1
                        res.append(result)
                    else:
                        result = 0
                        res.append(result)
            return res

        except Exception as e:
            print(e)

    def checkIndexOperator(self,operators):
        try:
            for idx, operator in enumerate(operators):
                if str(operator.lower()) == "and":
                    return idx, operator
        except Exception as e:
            print(e)

    def andOperations(self, res,idx,operator):
        try:
            if str(operator.lower()) == 'and':
                out = res[idx] and res[idx + 1]
                return out
        except Exception as e:
            print(e)

    def orOperations(self, operators, and_result, res, idx):
        try:
            if idx == 0:
                while idx+1 < len(operators):
                    if (operators[idx+1].lower()) == "or":
                        out=and_result or res[idx+2]
                        idx+=1
                    elif (operators[idx+1].lower()) == "and":
                        out=and_result and res[idx+2]
                        idx+=1
                return out
            elif idx == 1:
                while idx < len(operators):
                    if(operators[idx-1].lower()) == "or":
                        out=and_result or res[idx-1]
                        idx+=1
                    elif (operators[idx-1].lower()) == "and":
                        out=and_result and res[idx-1]
                        idx+=1
                return out
        except Exception as e:
            print(e)

    def getValuesFromDb(self, key):
        try:
            if key == 'Sinexcel_batt_inv_01:UserDataBlock1_tot_A':
                return 120
            if key == 'Sinexcel_batt_inv_01:UserDataBlock1_AphB':
                return 70
            if key == 'Sinexcel_batt_inv_01:UserDataBlock1_AphC':
                return 2500
        except Exception as e:
            print(e)

    def convertUTCtoUnix(self, times,keys):
        try:
            length = len(times)
            if length == 1:
                utctime=times[0].replace("'","")
                unixTime=time.mktime(datetime.datetime.strptime(utctime,"%d-%m-%Y %H:%M:%S").timetuple())
                print(unixTime)
                #initially do a minute minus and a minute plus
                #each time do a minute minus and a minute plus if we don't get any data from mrange
                for i in range(1,5):
                    timestamp =[]
                    timestamp.append(unixTime-i*60)
                    timestamp.append(unixTime+i*60)
                    get_data = self.mrangeDataRTS(keys,timestamp)
                    if len(get_data) == 3:
                        return get_data
                        break
            elif length > 1 :
                timestamp = []
                for i in range(length):
                    unixTime = time.mktime(datetime.datetime.strptime(times[i], "%d-%m-%Y %H:%M:%S.%f").timetuple())
                    timestamp.append(unixTime)
                return timestamp
        except Exception as e:
            print(e)

    def mrangeDataRTS(self,keys,timestamp):
        try:
            result = []
            for i in range(len(keys)):
                a = str(timestamp[0]) + '\t' + keys[i] + '\t' + str(timestamp[1])
                # print(a)
                rts = Client()
                # print(int(timestamp[0]),int(timestamp[1]))
                # print(keys[i])
                #filters – filter to match the time-series labels
                res=rts.range(keys[i],int(timestamp[0]),int(timestamp[1]))
                for elements in res:
                    value = (str(elements).strip("()").replace(',', '').split(' '))
                    key_value = value[1]
                    if key_value != None:
                        result.append(key_value)
                    else:
                        print("Error")
            return result
        except Exception as e:
            print(e)

def main():
    parser = argparse.ArgumentParser(prog='Alert Manager Interface', description='Alerts',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', '--set_priority', type=str, help='Give Priority Value', required=True)
    args = parser.parse_args()
    alert = Alerts(args.set_priority)
    values = alert.getKeysOperation()
    rts_keys, threshold, operator, operator1, result, time = values
    keys = rts_keys.split(",")
    thresholds = threshold.split(",")
    operators = operator.split(",")
    operator1 = operator1.split(",")
    if len(time) != 0:
        key_value=[]
        times=time.split(",")
        fetch_rts_data=alert.convertUTCtoUnix(times,keys)
        print(fetch_rts_data)
        for data in fetch_rts_data:
            key_value.append(int(float(data)))
        result = alert.compareOperations(key_value, thresholds, operators)
        print(result)
        idx, operator = alert.checkIndexOperator(operator1)
        print("Index is", idx)
        print("Operator is",operator)
        and_output = alert.andOperations(result, idx, operator)
        print(and_output)
        or_output = alert.orOperations(operator1, and_output, result, idx)
        print(or_output)
        #Operators Functions
    else:
        key = []
        for k in keys:
            result = alert.getValuesFromDb(k)
            key.append(result)
        result = alert.compareOperations(key, thresholds, operators)
        print(result)
        idx, operator = alert.checkIndexOperator(operator1)
        print("Index",idx)
        print("Operator",operator)
        and_output = alert.andOperations(result, idx, operator)
        print(and_output)
        or_output = alert.orOperations(operator1, and_output, result, idx)
        print(or_output)

if __name__ == "__main__":
    main()

