#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/home/pi/new_code

PIDFILE=/var/run/fronius_pub_01.pid
case $1 in
   start)
       # Launch your program as a detached process
       cd /home/pi/new_code/
       python3 "MqTT/MqTTPub.py" -c KSHS_fronius_inv_01 >> /home/pi/kshs_fronius_inv_pub_01.pid.log 2>&1 &
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

