#!/bin/sh
SCRIPT_DIR=$(cd $(dirname $0); pwd)

echo "install snowboy"
sudo apt-get install -y git portaudio19-dev python-pyaudio python3-pyaudio swig libatlas-base-dev
cd $SCRIPT_DIR/
git clone https://github.com/Kitt-AI/snowboy.git
cd $SCRIPT_DIR/snowboy/swig/Python3
make
cp snowboydetect.py $SCRIPT_DIR/
cp _snowboydetect.so $SCRIPT_DIR/
cd $SCRIPT_DIR
cp $SCRIPT_DIR/snowboy/resources/common.res $SCRIPT_DIR
rm -rf snowboy