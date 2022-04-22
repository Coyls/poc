#!/bin/sh
# launcher.sh
# Execute POC

cd /home/pi/Documents/poc
python3 ./server.py &
sleep 3
python3 ./tmp.py &
python3 ./proximity.py &
python3 ./rotary.py &
python3 ./ground-humidity.py &
sudo python3 ./switch.py &
