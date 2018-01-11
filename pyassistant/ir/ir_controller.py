import time
from ctypes import *
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pyassistant')
import infrared

class IRController():
    def __init__(self,scan_pin):
        self.scan_pin = scan_pin
        self.channels = {}
        self.send_repeat = 3

    def register_channel(self,name,send_pin):
        if name in self.channels:
            logger.warning('channel %s is already exists, it was overwritten')

        data = infrared.scan(send_pin, 40000)
        if len(data)<10:
            return False

        self.channels[name] = {
            'data':data,
            'pin':send_pin
        }

        return True

    def unregister_channel(self,name):
        if name not in self.channels:
            logger.error('channel %s did not register')
            return False
        del self.channels[name]
        return True

    def list_channels(self):
        return self.channels

    def send_channel(self,name):
        if name not in self.channels:
            logger.error('channel %s did not register')
            return False

        c = self.channels[name]
        infrared.send(c['data'],c['pin'],self.send_repeat,38000)
        return True



if __name__=='__main__':

    data = infrared.scan(27, 40000)
    import pprint
    pprint.pprint(data)

    while(True):
        print('Enter key to send')
        input()
        infrared.send(data,20,3,38000)
