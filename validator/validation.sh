#!/bin/bash

echo "Python Version Check"
check_python=$(python3 -V | awk '{print $2}')
if [ $check_python == "3.8.10" ]
then
  echo "Python Version is :-$check_python"
else
  echo "Installing Latest Python"
  apt install python3 -y
fi

echo "Check pip Version"
check_pip=$(pip3 --version | awk '{print $2}')
if [ $check_pip == "21.1.3" ]
then
  echo "Pip Version is :-$check_pip"
else 
  echo "Installing Latest Pip"
  apt-get install python3-pip
  pip install -U pip
fi

echo "Check Pymodbus Module"
check_pymodbus=$(pip list | grep pymodbus | awk '{print $1}')
if [ $check_pymodbus == "pymodbus" ]
then
  echo "Pymodbus Present as:-$check_pymodbus"
else
  echo "Downloading Pymodbus Module"
  pip install pymodbus
fi

echo "Check RedisTimeSeries Module"
redists=$(pip list | grep redistimeseries | awk '{print $1}')
if [ $redists == "redistimeseries" ]
then
  echo "RedisTimeSeries present as :-$redists"
else
  echo "Downloading RedisTimeSeries Module"
  pip install redistimeseries
fi

echo "Check Pytz Module"
pytz=$(pip list | grep pytz | awk '{print $1}')
if [ $pytz == "pytz" ]
then
  echo "Pytz present as :-$pytz"
else
  echo "Downloading Pytz Module"
  pip install pytz
fi

echo "Install Flatten Json"
flat_json=$(pip list | grep flatten-json | awk '{print $1}')
if [ $flat_json == "flatten-json" ]
then
  echo "FLatten-json present as :-$flat_json"
else
  echo "Downloading Flatten-json Module"
  pip install flatten-json
fi

echo "Install Python-DateUtil"
date_util=$(pip list | grep python-dateutil | awk '{print $1}')
if [ $date_util == "python-dateutil" ]
then
  echo "Date Util present as :-$date_util"
else
  echo "Downloading Date-Util Module"
  pip install python-dateutil
fi

echo "Install Datetime"
datetime=$(pip list | grep DateTime | awk '{print $1}')
if [ $datetime == "DateTime" ]
then
  echo "DateTime present as :-$datetime"
else
  echo "Downloading Date-Util Module"
  pip install Datetime
fi
