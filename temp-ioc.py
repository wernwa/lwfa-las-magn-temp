#!/usr/bin/python

from pcaspy import Driver, SimpleServer, Severity
import random
import thread
import serial
import sys
from setup import *

alive=True
prefix = 'shicane:'
pvdb={
    'temp_all' : {
        'type' : 'char',
        'count' : 100,
        'unit' : 'C',
    }
}
for name in ['q1','q2','q3','q4','q5','q6','q7','d1','d2']:
    pvdb['%s:temp'%name] = {
            'prec' : 2,
            'unit' : 'C',
            'low' : -20, 'high': 70,
            'lolo': -30,'hihi': 95,
            'lolim': -30, 'hilim': 100,
            'asg'  : 'readonly',
        }
tempcnt = 7

class myDriver(Driver):
    def  __init__(self):
        global tempcnt
        super(myDriver, self).__init__()

        try:
            self.ser = serial.Serial(tty_driver, baud, timeout=serial_timeout)
        except Exception as e:
            print e
            sys.exit(-1)

        # throw first lines away (i.a. not from the start)
        const=False
        tempcnt_prev=0
        tempcnt_prev2=0
        while const==False:
            line = self.ser.readline()
            sys.stdout.write(line)
            t_arr = line.split(' ')
            tempcnt = len(t_arr)-1
            if tempcnt == tempcnt_prev and tempcnt==tempcnt_prev2: const=True
            tempcnt_prev=tempcnt
            tempcnt_prev2=tempcnt_prev


        #t_arr = line.split(' ')
        tempcnt = len(t_arr)-1
        print '%d temperature sensors recognized'%tempcnt
        print '------------------------------'
        print ' Start polling (CTRL+C -> end).'
        print '------------------------------'
        self.tid = thread.start_new_thread(self.read_tty,())

    def read(self, reason):
        #if reason == 'RAND':
        #    value = random.random()
        #else:
        value = self.getParam(reason)
        return value


    def read_tty(self):

        global alive, tempcnt
        record_list=['q1:temp','q2:temp','q3:temp','q4:temp','q5:temp','q6:temp','q7:temp','d1:temp','d2:temp']

        while alive:
            try:
                line=''
                try:
                    line = self.ser.readline()
                except SerialException as e:
                    print e.strerror
                    line = 'None '*tempcnt+'\n'
                self.setParam('temp_all',line)
                #print line
                t_arr = line.split(' ')
                #print t_arr
                if (len(t_arr)!=tempcnt+1):
                    continue

                for i in range(0,tempcnt):
                    self.setParam(record_list[i],t_arr[i])
                self.updatePVs()
            except Exception as e:
                print 'Err:',e
                alive=False

if __name__ == '__main__':


    server = SimpleServer()
    server.initAccessSecurityFile('security.as', P=prefix)
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while alive:
        try:
            server.process(0.1)
        except KeyboardInterrupt:
            print " Bye"
            sys.exit()
