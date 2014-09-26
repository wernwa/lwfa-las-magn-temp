#!/usr/bin/python

from pcaspy import Driver, SimpleServer, Severity
import random
import thread
import serial

prefix = 'shicane:'
pvdb = {
#    'RAND' : {
#        'prec' : 3,
#        'scan' : 1,
#    },
    'q1:temp' : {
        'prec' : 3,
	'unit' : 'C',
#        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'q2:temp' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'q3:temp' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'q4:temp' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'q5:temp' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'q6:temp' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
    'q7:temp' : {
        'prec' : 3,
        'low' : -20, 'high': 70,
        'lolo': -30,'hihi': 99,
    },
#    'STATUS' : {
#        'type' : 'enum',
#        'enums':  ['OK', 'ERROR'],
#        'states': [Severity.NO_ALARM, Severity.MAJOR_ALARM]
#    },
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
	    #print line
            t_arr = line.split(' ')
            if (len(t_arr)!=tempcnt+1):
                continue
            #print t_arr
            self.setParam('q1:temp', t_arr[0])
            self.setParam('q2:temp', t_arr[1])
            self.setParam('q3:temp', t_arr[2])
            self.setParam('q4:temp', t_arr[3])
            self.setParam('q5:temp', t_arr[4])
            self.setParam('q6:temp', t_arr[5])
            self.setParam('q7:temp', t_arr[6])
            self.updatePVs()

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)

