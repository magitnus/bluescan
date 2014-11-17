# test BLE Scanning software
# jcs 6/8/2014

import fcntl, socket, struct
import requests
import blescan
import time
import sys

import bluetooth._bluetooth as bluez

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"
	print getHwAddr('eth0')

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

blescan.DEBUG=True

hostScript = "http://54.72.176.250/bp1/index.php"
macid = getHwAddr('eth0')

print macid

while True:
	returnedList = blescan.parse_events(sock, 6, hostScript, macid)

	print "----------"

	for beacon in returnedList:
		print beacon

        time.sleep(10);        

