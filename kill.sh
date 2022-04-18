#!/bin/sh
# launcher.sh
# Execute POC

cd /home/pi/Documents/poc
pkill -f server.py 
pkill -f tmp.py 
pkill -f proximity.py 
pkill -f rotary.py 
pkill -f ground-humidity.py &
sudo pkill -f switch.py 