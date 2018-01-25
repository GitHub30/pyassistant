#!/bin/sh

sudo apt-get -y update&&sudo apt-get -y upgrade
sudo apt-get install -y open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 open-jtalk

sudo pip3 install pyjtalk click
sudo pip3 install git+https://github.com/Microsoft/Cognitive-LUIS-Python.git

if [ -e ~/.pyassistant ]; then
else
    mkdir ~/.pyassistant
fi

echo "\
{\n\
                'COGNITIVE_SPEECH_KEY': '',\n\
                'COGNITIVE_LUIS_APPID': '',\n\
                'COGNITIVE_LUIS_APPKEY': '',\n\
                'COGNITIVE_SEARCH_KEY':'',\n\
                # snowboy or button\n\
                'ACTIVATION_TRIGGER': 'snowboy',\n\
                'RECORD_THRESHOLD': 4,\n\
                'RECORD_BEGIN_SECOND': 0.1,\n\
                'RECORD_END_SECOND': 1,\n\
                'TRIGGER_GPIO': 21,\n\
                'IR_SCAN_GPIO':27\n\
}\n\
">~/.pyassistant/setting.json