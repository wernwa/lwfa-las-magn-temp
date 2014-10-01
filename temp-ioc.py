#!/usr/bin/python

from pcaspy import Driver, SimpleServer, Severity
import random
import thread
import serial
import sys


prefix = 'shicane:'
pvdb={}
for name in ['q1','q2','q3','q4','q5','q6','q7','d1','d2']:
	pvdb['%s:temp'%name] = {
			'prec' : 2,
			'unit' : 'C',
			'low' : -20, 'high': 70,
			'lolo': -30,'hihi': 99,
		}
tempcnt = 7

class myDriver(Driver):
	def  __init__(self):
		global tempcnt
		super(myDriver, self).__init__()
		self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

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

		global tempcnt
 		record_list=['q1:temp','q2:temp','q3:temp','q4:temp','q5:temp','q6:temp','q7:temp','d1:temp','d2:temp']

		while True:
			line = self.ser.readline()
			#print line
			t_arr = line.split(' ')
			#print t_arr
			if (len(t_arr)!=tempcnt+1):
				continue

			for i in range(0,tempcnt):
				self.setParam(record_list[i],t_arr[i])
			self.updatePVs()

if __name__ == '__main__':
	server = SimpleServer()
	server.createPV(prefix, pvdb)
	driver = myDriver()

	# process CA transactions
	while True:
		try:
			server.process(0.1)
		except KeyboardInterrupt:
			print " Bye"
			sys.exit()
