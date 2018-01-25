#!/bin/sh

sudo apt-get -y update&&sudo apt-get -y upgrade
sudo apt-get install -y open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 open-jtalk

sudo pip3 install pyjtalk click
sudo pip3 install git+https://github.com/Microsoft/Cognitive-LUIS-Python.git