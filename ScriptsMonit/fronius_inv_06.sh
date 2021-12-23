#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/home/pi/new_code:/home/pi

PIDFILE=/var/run/fronius_inv_06.pid
case $1 in
   start)
       # Launch your program as a detached process
       python3 "/home/pi/new_code/Modbus/ModbusPolling.py" -d Fronius_inv_06 -l UserDataBlock1 -l ReadWriteBlock1 >> /home/pi/fronius_inv_06.pid.log 2>&1 &
       # Get its PID and store it
       echo $! > ${PIDFILE}
   ;;
   stop)
      kill `cat ${PIDFILE}`
      # Now that it's killed, don't forget to remove the PID file
      rm ${PIDFILE}
   ;;
   *)
      echo "usage: scraper {start|stop}" ;;
esac
exit 0