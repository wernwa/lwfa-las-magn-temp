#!/usr/bin/python

import serial
import random
import time

# system call to socat:
#socat -d -d pty,raw,echo=1 pty,raw,echo=1


tty_name='/dev/pts/16'


s = serial.Serial(tty_name)


while True:
    line = ''
    for i in range(1,10):
        temp=random.random()
        line+='%.2f '%temp
        time.sleep(0.5)
    line+='\n'
    print line
    s.write(line)
