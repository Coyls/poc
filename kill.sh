#!/bin/sh
# launcher.sh
# Execute POC

cd /home/pi/Documents/poc
sudo pkill -f server.py 
sudo pkill -f tmp.py 
sudo pkill -f proximity.py 
sudo pkill -f rotary.py 
sudo pkill -f ground-humidity.py &
sudo pkill -f switch.py 