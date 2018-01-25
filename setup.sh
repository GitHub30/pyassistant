#!/bin/sh
CURRENT=`pwd`
SCRIPT_DIR=$(cd $(dirname $0); pwd)

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 open-jtalk
sudo apt-get install -y git portaudio19-dev python-pyaudio python3-pyaudio swig libatlas-base-dev sox

if [ "`python --version 2>&1| cut -d . -f 1`" = "Python 2" ]; then
    sudo pip3 install pyjtalk click requests
    sudo pip3 install git+https://github.com/Microsoft/Cognitive-LUIS-Python.git
else
    pip install pyjtalk click requests
    pip install git+https://github.com/Microsoft/Cognitive-LUIS-Python.git
fi

#cd $SCRIPT_DIR/
#git clone https://github.com/Kitt-AI/snowboy.git
#cd $SCRIPT_DIR/snowboy/swig/Python3
#make
#cp -f snowboydetect.py $SCRIPT_DIR/pyassistant/trigger
#cp -f _snowboydetect.so $SCRIPT_DIR/pyassistant/trigger
#cd $SCRIPT_DIR
#cp -f $SCRIPT_DIR/snowboy/resources/common.res $SCRIPT_DIR/pyassistant/trigger
#rm -rf snowboy

if [ -e ~/.pyassistant ]; then
    :
else
    mkdir ~/.pyassistant
fi

echo "\
{\n\
                \"COGNITIVE_SPEECH_KEY\": \"\",\n\
                \"COGNITIVE_LUIS_APPID\": \"\",\n\
                \"COGNITIVE_LUIS_APPKEY\": \"\",\n\
                \"COGNITIVE_SEARCH_KEY\":\"\",\n\
                \"ACTIVATION_TRIGGER\": \"snowboy\",\n\
                \"RECORD_THRESHOLD\": 4,\n\
                \"RECORD_BEGIN_SECOND\": 0.1,\n\
                \"RECORD_END_SECOND\": 1,\n\
                \"TRIGGER_GPIO\": 21,\n\
                \"IR_SCAN_GPIO\":27,\n\
                \"MIC_CARD_ID\":2,\n\
                \"MIC_DEVICE_ID\":0,\n\
                \"SPEAKER_CARD_ID\":1,\n\
                \"SPEAKER_DEVICE_ID\":0\n\
}\n\
">~/.pyassistant/setting.json

echo "please edit ~/.pyassistant/setting.json"

cd $CURRENT