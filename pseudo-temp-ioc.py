#!/usr/bin/python

from pcaspy import Driver, SimpleServer, Severity
import random
import thread
import serial
import sys
import time

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
tempcnt = 9

class myDriver(Driver):
    def  __init__(self):
        global tempcnt
        super(myDriver, self).__init__()


        #t_arr = line.split(' ')
        print '%d temperature sensors recognized'%tempcnt
        print '------------------------------'
        print ' Pseudo temperature ioc, Start polling (CTRL+C -> end).'
        print '------------------------------'
        self.tid = thread.start_new_thread(self.read_tty,())

    def read(self, reason):
        #if reason == 'RAND':
        #    value = random.random()
        #else:
        value = self.getParam(reason)
        return value


    def read_tty(self):

        global tempcnt
        record_list=['q1:temp','q2:temp','q3:temp','q4:temp','q5:temp','q6:temp','q7:temp','d1:temp','d2:temp']
        def rt(prev_q_index):
            prev = float(self.getParam('%s'%record_list[prev_q_index]))
            s=random.randint(0,1)
            if s==0: sign=-1
            else: sign=1
            return prev + sign*random.random()

        while True:
            line='%.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f \n'%(rt(0),rt(1),rt(2),rt(3),rt(4),rt(5),rt(6),rt(7),rt(8))
            self.setParam('temp_all',line)
            #print line
            t_arr = line.split(' ')
            #print t_arr
            if (len(t_arr)!=tempcnt+1):
                continue

            for i in range(0,tempcnt):
                self.setParam(record_list[i],t_arr[i])

            self.updatePVs()
            time.sleep(0.5)

if __name__ == '__main__':


    server = SimpleServer()
    server.initAccessSecurityFile('security.as', P=prefix)
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        try:
            server.process(0.1)
        except KeyboardInterrupt:
            print " Bye"
            sys.exit()
