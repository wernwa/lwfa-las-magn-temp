#!/bin/bash

export EPICS_CA_SERVER_PORT=5064
export EPICS_CA_REPEATER_PORT=5065


if [ "$1" == "start" ]
then
    ./temp-ioc.py
elif [ "$1" == "stop" ]
then
    
    killall -9 ./temp-ioc.py
    killall -9 ./temp-ioc.sh

    fuser -k $EPICS_CA_SERVER_PORT/tcp
    fuser -k $EPICS_CA_REPEATER_PORT/udp
else
    echo "usage: ./temp_ioc.sh start|stop"
fi
