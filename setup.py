
cycle_temperature = 80.0
#tty_driver = '/dev/pts/17'
tty_driver = '/dev/ttyACM0'
baud = 115200
serial_timeout = 1 # sec


# assignment of the temperatur sensor NR to the magnet EPICs name
name_to_index = {
    'q1:temp': 1,
    'q2:temp': 2,
    'q3:temp': 3,
    'q4:temp': 4,
    'q5:temp': 5,
    'q6:temp': 6,
    'q7:temp': 7,
    'd1:temp': 8,
    'd2:temp': 9,
}
