#!/usr/bin/env python

from pcaspy import Driver, SimpleServer, Severity
import random
import thread
import serial

prefix = 'SHICANE:'
pvdb = {
    'RAND' : {
        'prec' : 3,
        'scan' : 1,
    },
    'M1:T' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'M2:T' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'M3:T' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'M4:T' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'M5:T' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'M6:T' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'M7:T' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'STATUS' : {
        'type' : 'enum',
        'enums':  ['OK', 'ERROR'],
        'states': [Severity.NO_ALARM, Severity.MAJOR_ALARM]
    },
}
tempcnt = 7

class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.tid = thread.start_new_thread(self.read_tty,())


    def read(self, reason):
        if reason == 'RAND':
            value = random.random()
        else:
            value = self.getParam(reason)
        return value

    def read_tty(self):
        global tempcnt
        while True:
            line = self.ser.readline()
            t_arr = line.split(' ')
            if (len(t_arr)!=tempcnt+1):
                continue
            #print t_arr
            self.setParam('M1:T', t_arr[0])
            self.setParam('M2:T', t_arr[1])
            self.setParam('M3:T', t_arr[2])
            self.setParam('M4:T', t_arr[3])
            self.setParam('M5:T', t_arr[4])
            self.setParam('M6:T', t_arr[5])
            self.setParam('M7:T', t_arr[6])
            self.updatePVs()

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)

