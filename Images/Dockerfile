FROM ubuntu:20.04

RUN apt update && apt install python3 -y 

RUN apt install python3-pip -y  && pip install -U pip

RUN pip install pymodbus && pip install redistimeseries && pip install pytz

RUN pip install flatten-json && pip install python-dateutil

RUN pip install DateTime

RUN apt install curl -y && apt install unzip -y && apt install redis-server -y && apt install lsof -y

RUN curl "https://s3.amazonaws.com/redismodules/redistimeseries/redistimeseries.Linux-x86_64.1.4.10.zip" -o "redistimeseries.Linux-x86_64.1.4.10.zip"

RUN unzip -o redistimeseries.Linux-x86_64.1.4.10.zip && cp -rp redistimeseries.so /etc/redis/


RUN curl "https://www.modbusdriver.com/downloads/diagslave.tgz" -o "diagslave-3.2.tgz"


RUN tar xzf  diagslave-3.2.tgz

RUN mkdir x86_64-linux-gnu

RUN cd diagslave && cp -rp x86_64-linux-gnu/diagslave   ../x86_64-linux-gnu/diagslave 

RUN rm -rf diagslave 

ENV PATH="$PATH:./x86_64-linux-gnu"


