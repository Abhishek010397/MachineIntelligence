#!/bin/bash

echo "Python Version Check"
check_python=$(python3 -V | awk '{print $2}')
if [ $check_python == "3.5.3" ] || [ $check_python == "3.8.10" ]
then
  echo "Python Version is :-$check_python"
else
  echo "Installing Latest Python"
  apt-get install python3 -y
fi

echo "Check pip Version"
check_pip=$(python3 -m pip -V | awk '{print $2}')
if [ $check_pip == "9.0.1" ] || [ $check_pip == "21.1.3" ]
then
  echo "Pip Version is :-$check_pip"
else 
  echo "Installing Latest Pip"
  apt-get install python3-pip
fi

echo "Check Pymodbus Module"
check_pymodbus=$(python3 -m pip list | grep pymodbus | awk '{print $1}')
if [ $check_pymodbus == "pymodbus" ]
then
  echo "Pymodbus Present as:-$check_pymodbus"
else
  echo "Downloading Pymodbus Module"
  python3 -m pip install pymodbus
fi

echo "Check RedisTimeSeries Module"
redists=$(python3 -m pip list | grep redistimeseries | awk '{print $1}')
if [ $redists == "redistimeseries" ]
then
  echo "RedisTimeSeries present as :-$redists"
else
  echo "Downloading RedisTimeSeries Module"
  python3 -m pip install redistimeseries
fi

echo "Check Pytz Module"
pytz=$(python3 -m pip list | grep pytz | awk '{print $1}')
if [ $pytz == "pytz" ]
then
  echo "Pytz present as :-$pytz"
else
  echo "Downloading Pytz Module"
  python3 -m pip install pytz
fi

echo "Install Flatten Json"
flat_json=$(python3 -m pip list | grep flatten-json | awk '{print $1}')
if [ $flat_json == "flatten-json" ]
then
  echo "Flatten-json present as :-$flat_json"
else
  echo "Downloading Flatten-json Module"
  python3 -m pip install flatten-json
fi

echo "Install Python-DateUtil"
date_util=$(python3 -m pip list | grep python-dateutil | awk '{print $1}')
if [ $date_util == "python-dateutil" ]
then
  echo "Date Util present as :-$date_util"
else
  echo "Downloading Date-Util Module"
  python3 -m pip install python-dateutil
fi

echo "Install Datetime"
datetime=$(python3 -m pip list | grep DateTime | awk '{print $1}')
if [ $datetime == "DateTime" ]
then
  echo "DateTime present as :-$datetime"
else
  echo "Downloading Date-Util Module"
  python3 -m pip install Datetime
fi

echo "Install MqTT"
mqtt=$(python3 -m pip list | grep paho-mqtt | awk '{print $1}')
if [ $mqtt == "paho-mqtt" ]
then
  echo "Mqtt present as :-$mqtt"
else
  echo "Downloading MqTT Module"
  python3 -m pip install paho-mqtt
fi

