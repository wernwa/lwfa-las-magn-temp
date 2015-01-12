#!/usr/bin/python
#
#   writes temperature (as random values) to a virtual tty
#   start socat as described below and change setup.py and this file
#   to the right /dev/... driver name
import sys
import serial
import random
import time
import epics
import traceback




# system call to socat:
#
# socat -d -d pty,raw,echo=1 pty,raw,echo=1
#2000/01/03 12:20:52 socat[2185] N PTY is /dev/pts/3
#2000/01/03 12:20:52 socat[2185] N PTY is /dev/pts/9
#2000/01/03 12:20:52 socat[2185] N starting data transfer loop with FDs [3,3] and [5,5]
#
# The first pty is for writing (virtual-tty-writer.py)
# the second is for reading (setup.py)

try:
    pty_nr=int(sys.argv[1]) # get the pty number from command line
except IndexError:
    print 'usage: %s <ptynr>'%sys.argv[0]
    sys.exit(-1)


s = serial.Serial('/dev/pts/%d'%pty_nr)

temp=[0,0,0,0,0,0,0,0,0]
#temp=[75,75,75,75,75,75,75,75,75]

curr=[0,0,0,0,0,0,0,0,0]

def onPVChanges(pvname=None, value=None, timestamp=None, **kw):

    arr = value.tostring().split(' ')
    try:
        for i in range(0,len(curr)):
            try:
                curr[i] = abs(float(arr[i]))
            except:
                curr[i] = 0

    except Exception as e:
        print traceback.format_exc()


magn_curr_all = epics.PV('chicane:magn_curr_all', auto_monitor=True )
magn_curr_all.add_callback(onPVChanges)

curr_max = 6.0



while True:
    line = ''
    for i in range(0,len(temp)):
        if random.random()>0.5: sign=1
        else: sign=-1
        if temp[i]<20: entropy=1
        elif temp[i]>20: entropy=-1
        else: entropy=0
        temp[i]=temp[i]+random.random()*0.2*entropy+random.random()*sign*0.1+curr[i]/curr_max
        #if i==0: temp[i]-=200   # test rearange
        line+='%.2f '%temp[i]
    line+='\n'
    s.write(line)
    time.sleep(0.5)
