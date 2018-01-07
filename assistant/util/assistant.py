import os
import json
import logging
import traceback
logger = logging.getLogger('pi-assistant')

class Assistant():

    def __init__(self):
        self.home = os.environ['HOME']
        self.config_dir = os.path.join(self.home, '.pi-assistant')
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

        self.setting_file = os.path.join(self.config_dir, 'setting.json')
        if os.path.exists(self.setting_file):
            with open(self.setting_file, 'r') as f:
                self.setting = json.load(f)
        else:
            self.setting = {
                'COGNITIVE_SPEECH_KEY':{
                    'type':'string',
                    'value':'',
                    'description':''
                },
                'COGNITIVE_LUIS_APPID': {
                    'type': 'string',
                    'value': '',
                    'description':''
                },
                'COGNITIVE_LUIS_APPKEY': {
                    'type': 'string',
                    'value': '',
                    'description':''
                },
                'ACTIVATION_TRIGGER':{
                    'type':'select',
                    'value':
                        {
                            'value':'snowboy',
                            'label':'snowboy hotword detection'
                        },
                    'option':[
                        {
                            'value':'snowboy',
                            'label':'snowboy hotword detection'
                        },
                        {
                            'value':'button',
                            'label':'GPIO button trigger'
                        }
                    ],
                    'description':''
                },
                'RECORD_THRESHOLD':{
                    'type':'slider',
                    'value':4,
                    'min':0,
                    'max':100,
                    'step':1,
                    'description':''
                },
                'RECORD_BEGIN_SECOND': {
                    'type': 'slider',
                    'value': 0.1,
                    'min': 0,
                    'max': 5,
                    'step':0.1,
                    'description':''
                },
                'RECORD_END_SECOND': {
                    'type': 'slider',
                    'value': 1,
                    'min': 0,
                    'max': 5,
                    'step': 0.1,
                    'description':''
                },
                'TRIGGER_GPIO':{
                    'type':'select',
                    'value':{},
                    'option':[]
                }
            }
            for i in range(27):
                current = i+1
                obj = {
                        'value':current,
                        'label':'GPIO %d'%current
                    }
                if current>1:
                    self.setting['TRIGGER_GPIO']['option'].append(obj)
                    if current == 21:
                        self.setting['TRIGGER_GPIO']['value'] = obj

    def __enter__(self):


        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.error(exc_type)
        logger.error(exc_val)
        traceback.print_tb(exc_tb)
        with open(self.setting_file, 'w') as f:
            json.dump(self.setting,f)

        return False