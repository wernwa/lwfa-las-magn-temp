# 1 ? not working now
lsusb
    Bus 001 Device 004: ID 2341:0043 Arduino SA Uno R3 (CDC ACM)
    ...
grep 2341 /sys/bus/usb/devices/*/uevent

sudo sh -c "echo 0 > /sys/bus/usb/devices/1-3.3/authorized"
sudo sh -c "echo 1 > /sys/bus/usb/devices/1-3.3/authorized"

# 2 ?
sudo sh -c "echo -n '1-3.3' > /sys/bus/usb/drivers/usb/unbind"
sudo sh -c "echo -n '1-3.3' > /sys/bus/usb/drivers/usb/bind"

# get ID:BUS from lsusb
sudo ./usbreset /dev/bus/usb/001/009

# Funktioniert!!!!
# switch usb power off/on
sudo sh -c 'echo "1-3.3" > /sys/bus/usb/drivers/usb/unbind'
sudo sh -c 'echo "1-3.3" > /sys/bus/usb/drivers/usb/bind'
# set the baud speed of the tty
sudo stty -F /dev/ttyACM0 115200
