#!/usr/bin/python

import os, sys
import re
from setup import *
import time



#usb_out = os.system('lsusb')
usb_out = os.popen('lsusb').read()

m = re.search('Bus (\d+) Device (\d+): ID .*? Arduino.*?',usb_out)
if m==None:
    print 'Err1: no Arduino Board found'
    sys.exit()
else:
    bus=m.group(1)
    dev=m.group(2)
    osstr='grep bus/usb/%s/%s /sys/bus/usb/devices/*/uevent'%(bus,dev)
    grep_out = os.popen(osstr).read()
    m = re.search('/sys/bus/usb/devices/(.*?)/uevent.*',grep_out)
    if m==None:
        print 'Err2: no Arduino Board found'
        sys.exit()
    else:
        dev_nr=m.group(1)
        print 'resetting device NR',dev_nr
        os.system('sudo rm %s'%tty_driver) # remove driver in dev bevore reinit
        #os.system('sudo sh -c \'echo 0 > /sys/bus/usb/devices/%s/authorized\''%dev_nr)
        os.system('sudo sh -c \'echo "%s" > /sys/bus/usb/drivers/usb/unbind\''%dev_nr)
        time.sleep(0.5)
        os.system('sudo sh -c \'echo "%s" > /sys/bus/usb/drivers/usb/bind\''%dev_nr)
        time.sleep(0.5)
        #os.system('sudo sh -c \'echo 1 > /sys/bus/usb/devices/%s/authorized\''%dev_nr)
        os.system('sudo stty -F %s %s'%(tty_driver,baud))


