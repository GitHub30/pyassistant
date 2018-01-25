#!/bin/sh

sudo apt-get -y update&&sudo apt-get -y upgrade
sudo apt-get install -y open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 open-jtalk

sudo pip3 install pyjtalk click
sudo pip3 install git+https://github.com/Microsoft/Cognitive-LUIS-Python.git

mkdir ~/.pyassistant
echo "\
{\
                'COGNITIVE_SPEECH_KEY': '',\
                'COGNITIVE_LUIS_APPID': '',\
                'COGNITIVE_LUIS_APPKEY': '',\
                'COGNITIVE_SEARCH_KEY':'',\
                # snowboy or button\
                'ACTIVATION_TRIGGER': 'snowboy',\
                'RECORD_THRESHOLD': 4,\
                'RECORD_BEGIN_SECOND': 0.1,\
                'RECORD_END_SECOND': 1,\
                'TRIGGER_GPIO': 21,\
                'IR_SCAN_GPIO':27\
            }\
"\>~/.pyassistant/setting.json