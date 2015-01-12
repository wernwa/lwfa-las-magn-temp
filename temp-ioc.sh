#!/bin/bash

#
#   set the two variables to free ports
#
export EPICS_CA_SERVER_PORT=20002
export EPICS_CA_REPEATER_PORT=20003


if [ "$1" == "start" ]
then
    ./temp-ioc.py
elif [ "$1" == "stop" ]
then
    
    killall -9 ./temp-ioc.py
    killall -9 ./temp-ioc.sh

    fuser -k $EPICS_CA_SERVER_PORT/tcp
    fuser -k $EPICS_CA_REPEATER_PORT/udp
elif [ "$1" == "reset" ]
then
    ## switch usb power off/on
    #sudo sh -c 'echo "1-3.3" > /sys/bus/usb/drivers/usb/unbind'
    #sudo sh -c 'echo "1-3.3" > /sys/bus/usb/drivers/usb/bind'
    ## set the baud speed of the tty
    #sudo stty -F /dev/ttyACM0 115200
    ./reset-usb.py

else
    echo "usage: ./temp_ioc.sh start|stop|reset"
fi
