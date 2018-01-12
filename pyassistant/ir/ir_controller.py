import json
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pyassistant')
import pyassistant.ir.infrared as infrared

class IRController():
    def __init__(self,scan_pin,config_dir):
        self.scan_pin = scan_pin
        self.channels = {}
        self.config_dir = config_dir
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
        self.config_path = os.path.join(self.config_dir,'channels.json')

        if os.path.exists(self.config_path):
            self.__load()

    def __save(self):
        with open(self.config_path,'w') as f:
            json.dump(self.channels,f)

    def __load(self):
        with open(self.config_path,'r') as f:
            self.channels = json.load(f)

    def register_channel(self,name,send_pin):
        if name in self.channels:
            logger.warning('channel %s is already exists, it was overwritten')

        data = infrared.scan(self.scan_pin, 40000)
        if len(data)<10:
            return False

        self.channels[name] = {
            'data':data,
            'pin':send_pin
        }

        self.__save()

        return True

    def unregister_channel(self,name):
        if name not in self.channels:
            logger.error('channel %s did not register')
            return False
        del self.channels[name]
        self.__save()
        return True

    def list_channels(self):
        return self.channels

    def get_channel(self,name):
        return self.channels[name]

    def send_channel(self,name,send_repeat=3):
        if name not in self.channels:
            logger.error('channel %s did not register')
            return False

        c = self.channels[name]
        infrared.send(c['data'],c['pin'],send_repeat,38000)
        return True



if __name__=='__main__':

    data = infrared.scan(27, 40000)
    import pprint
    pprint.pprint(data)

    while(True):
        print('Enter key to send')
        input()
        infrared.send(data,20,3,38000)
