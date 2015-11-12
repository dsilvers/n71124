#! /bin/sh

sleep 30
udevadm trigger -subsystem-match=usb
sleep 30
wvdial &
exit 0
