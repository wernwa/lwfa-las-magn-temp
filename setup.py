
cycle_temperature = 80.0
#tty_driver = '/dev/pts/17'
tty_driver = '/dev/ttyACM0'
baud = 115200
serial_timeout = 1 # sec


# assignment of the temperatur sensor NR to the magnet EPICs name
name_to_index = {
    'q1:temp': 3,
    'q2:temp': 4,
    'q3:temp': 5,
    'q4:temp': 6,
    'q5:temp': 7,
    'q6:temp': 8,
    'q7:temp': 9,
    'd1:temp': 1,
    'd2:temp': 2,
}
