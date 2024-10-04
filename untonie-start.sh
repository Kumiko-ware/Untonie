#!/bin/bash

cd /home/untonie
#mpg123 -a bluealsa -q -R --fifo /tmp/player.pipe > /tmp/player.out &
mpg123  -q -R --fifo /tmp/player.pipe > /tmp/player.out &
source untonie-py-env/bin/activate
python untonie.py 
