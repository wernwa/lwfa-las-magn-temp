# 1 ? not working now
sudo sh -c "echo 0 > /sys/bus/usb/devices/1-3.3/authorized"
sudo sh -c "echo 1 > /sys/bus/usb/devices/1-3.3/authorized"

# 2 ?
sudo sh -c "echo -n '1-3.3' > /sys/bus/usb/drivers/usb/unbind"
sudo sh -c "echo -n '1-3.3' > /sys/bus/usb/drivers/usb/bind"

# get ID:BUS from lsusb
sudo ./usbreset /dev/bus/usb/001/009
