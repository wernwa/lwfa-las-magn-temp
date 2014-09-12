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
    'T1' : {
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
        while True:
            line = self.ser.readline()
            t_arr = line.split(' ')
            self.setParam('T1', t_arr[0])
            self.updatePVs()

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)

