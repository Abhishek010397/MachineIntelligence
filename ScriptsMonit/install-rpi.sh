#!/bin/bash

echo "************************************Check for Updates****************************************************************"
sudo apt update
sudo apt install -y build-essential checkinstall

echo "***************************************Download Redis-Cli If Not Present***********************************************"
version=$(redis-server --version | awk '{print $3}' | sed 's/^.*=//')
if [ -z "$version"  ]
then 
    echo '**************Downloading Redis CLI*****************'
    cd /home/pi
    pwd
    sudo rm -rf /home/pi/redis-stable
    wget -O /home/pi/redis-stable.tar.gz http://download.redis.io/redis-stable.tar.gz
    cd /home/pi && tar -xf redis-stable.tar.gz -C /home/pi/
    pwd
    cd /home/pi/redis-stable
    make -j$(nproc)
    sudo checkinstall
    redis-server --version
else
  echo "Already Present"
  echo "Version is:-" $version
fi

echo "***************************************Downloading Redis-Time Module If Not Present*************************************"

directory=$(ls /home/pi/ | grep RedisTimeSeries)
if [ -z "$directory" ]
then
    echo "**************Downloading RedisTimeSeries Module****************"
    wget -O /home/pi/RedisTimeSeries.tar.xz https://redistimeseries.s3.amazonaws.com/RedisTimeSeries.tar.xz
    cd /home/pi && tar -xf RedisTimeSeries.tar.xz -C /home/pi/
    cd /home/pi/RedisTimeSeries && ./deps/readies/bin/getpy3 && make build
    ls /home/pi/RedisTimeSeries/bin | grep redistimeseries.so
else
  echo "Already Present"
  echo $directory
fi

echo "****************************************Downloading Monit If Not Present***************************************************"

monit_version=$(monit -V | awk 'NR==1 {print $5}')
if [ -z "$monit_version" ]
then
    echo "****************Downloading Monit*********************************"
    sudo apt install -y monit
    monit -V
else
  echo "Already Present"
  echo "Version is:-" $monit_version
fi
