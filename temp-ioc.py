#!/usr/bin/python

from pcaspy import Driver, SimpleServer, Severity
import random
import thread
import serial
import sys
from setup import *
import epics
import time
from termcolor import colored
import traceback

alive=True
demag_pv = epics.PV('chicane:demag')
prefix = 'chicane:'
pvdb={
    'temp_all' : {
        'type' : 'char',
        'count' : 100,
        'unit' : 'C',
    },
    'zps:switchbox' : {
        'type' : 'int',
    },
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


ser_lock = thread.allocate_lock()

class myDriver(Driver):
    def  __init__(self):
        global tempcnt
        super(myDriver, self).__init__()

        try:
            self.ser = serial.Serial(tty_driver, baud, timeout=serial_timeout)
        except Exception as e:
            print traceback.format_exc()
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


        self.trigger_demag_active=False

        #t_arr = line.split(' ')
        tempcnt = len(t_arr)-1
        if tempcnt==0:
            print colored('Err:','red'),'no numbers for the temperature recognized. exiting'
            sys.exit(-1)
        print '%d temperature sensors recognized'%tempcnt
        print '------------------------------'
        print ' Start polling (CTRL+C -> end).'
        print '------------------------------'
        self.tid = thread.start_new_thread(self.read_tty,())

    def read(self, reason):

        # read the power status of the magnets
        if reason=='zps:switchbox':
            value = 99
            ser_lock.acquire()
            self.ser.write(chr(2))
            line = self.ser.readline()
            ser_lock.release()
            arr = line.split()
            if arr[0]=='zps:switchbox':
                #print 'status: %s'%arr[1]
                if arr[1]=='0': value=0
                elif arr[1]=='1': value=1
        else:
            value = self.getParam(reason)

        return value


    def read_tty(self):

        global alive, tempcnt, name_to_index
        record_list=['q1:temp','q2:temp','q3:temp','q4:temp','q5:temp','q6:temp','q7:temp','d1:temp','d2:temp']

        index_rearanged = [99,99,99,99,99,99,99,99,99]
        for i in range(0,tempcnt):
            index_rearanged[i] = name_to_index[record_list[i]]-1


        while alive:
            try:
                line=''
                try:
                    ser_lock.acquire()
                    line = self.ser.readline()
                    ser_lock.release()
                except Exception as e:
                    #print e.strerror
                    line = 'None '*tempcnt+'\n'
                    print traceback.format_exc()
                t_arr = line.split(' ')
                #print t_arr
                if (len(t_arr)!=tempcnt+1):
                    continue

                start_demag=False
                line = ''
                for i in range(0,tempcnt):
                    rear_i = index_rearanged[i]
                    t_str = t_arr[rear_i]
                    t = float(t_str)
                    line += t_str+' '
                    if t>cycle_temperature:
                        start_demag=True
                        print colored('critical temperature of %.2f degree reached for %s'%(t,record_list[i]), 'red')
                    self.setParam(record_list[i],t)
                    #if i==0: print i,rear_i,record_list[i],t

                #print line
                self.setParam('temp_all',line)

                if start_demag==True:
                    self.trigger_demag()

                self.updatePVs()
            except Exception as e:
                #print 'Err:',e
                alive=False
                print traceback.format_exc()

    def trigger_demag(self):

        def trigger():
            self.trigger_demag_active=True
            print 'triggering the cycling for all magnets'
            demag_pv.put(1)
            time.sleep(15)
            self.trigger_demag_active=False

        if self.trigger_demag_active==False:
            thread.start_new_thread(trigger,())



    def write(self, reason, value):
        status = False
        # turn the power of the powersupplies on/off
        if reason == 'zps:switchbox':
            print 'zps:switchbox',value
            ser_lock.acquire()
            if value==1:
                self.ser.write(chr(1))
            elif value==0:
                self.ser.write(chr(0))
            ser_lock.release()

            status = True
            # store the value and this also resets alarm status and severity for string type
            self.setParam(reason, value)
        else:
            status = True
            # store the value and this also resets alarm status and severity for string type
            self.setParam(reason, value)

        return status

if __name__ == '__main__':


    server = SimpleServer()
    server.initAccessSecurityFile('security.as', P=prefix)
    server.createPV(prefix, pvdb)
    driver = myDriver()

    start_ts = time.time()

    # process CA transactions
    while alive:
        try:
            server.process(0.1)
            ts = time.time() - start_ts
            sys.stdout.write('%d s\r'%int(round(ts)))
            sys.stdout.flush()
        except KeyboardInterrupt:
            print " Bye"
            sys.exit()
