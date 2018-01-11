#!/bin/sh
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR
g++ -I/usr/include/python3.5 -DPIC -shared -fPIC -o infrared.so infrared.cpp -lwiringPi