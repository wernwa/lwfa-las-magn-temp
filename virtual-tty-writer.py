#!/usr/bin/python

import serial
import random
import time

# system call to socat:
#
# socat -d -d pty,raw,echo=1 pty,raw,echo=1
#2000/01/03 12:20:52 socat[2185] N PTY is /dev/pts/3
#2000/01/03 12:20:52 socat[2185] N PTY is /dev/pts/9
#2000/01/03 12:20:52 socat[2185] N starting data transfer loop with FDs [3,3] and [5,5]
#
# The first pty is for writing (virtual-tty-writer.py)
# the second is for reading (setup.py)
pty_nr=3


s = serial.Serial('/dev/pts/3')

temp=[0,0,0,0,0,0,0,0,0]

while True:
    line = ''
    for i in range(0,len(temp)):
        if random.random()>0.5: sign=1 
        else: sign=-1
        temp[i]=temp[i]+sign*random.random()
        line+='%.2f '%temp[i]
    line+='\n'
    s.write(line)
    time.sleep(0.5)
