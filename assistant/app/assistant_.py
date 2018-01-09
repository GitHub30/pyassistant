import os
import json
import logging
import traceback
import assistant.util.alsa as alsa
import assistant.util.process as process
logger = logging.getLogger('pi-assistant')

class Assistant():

    def __init__(self):
        self.home = os.environ['HOME']
        self.is_active = True
        self.is_mute = False
        self.config_dir = os.path.join(self.home, '.pi-assistant')
        self.on_sound_path = os.path.join(os.path.dirname(__file__), '../resource/trigger_on.wav')
        self.off_sound_path = os.path.join(os.path.dirname(__file__), '../resource/trigger_off.wav')
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

        self.clients = []

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        logger.error(exc_type)
        logger.error(exc_val)
        traceback.print_tb(exc_tb)
        with open(self.setting_file, 'w') as f:
            json.dump(self.setting,f,ensure_ascii=False,indent=2)

        return False

    def open(self):
        print('open')
        if self not in self.clients:
            self.clients.append(self)

    def on_message(self, msg):
        print(msg)
        msg = json.loads(msg)
        try:
            res = self.process_command(msg['command'], msg['detail'])

            if res != None:
                res_msg = {
                    'command': msg['command'],
                    'detail': res
                }
                self.write_message(json.dumps(res_msg))
        except Exception as e:
            res_msg = {
                'command': 'ASSISTANT_ERROR',
                'detail': {
                    'message': e.args
                }
            }
            self.write_message(json.dumps(res_msg))
            logger.error(e.args[0])
            logger.error(traceback.format_exc())

    def on_close(self):
        print('close')
        if self in self.clients:
            self.clients.remove(self)


    def process_command(self,command, detail):

        if command == 'ASSISTANT_RESTART':
            self.say('再起動します')
            self.stop()
            return {}
        if command == 'ASSISTANT_MUTE':
            if detail['isMute']:
                self.is_mute = True
                self.say('マイクはオフです')
                logger.info('mute on')
            else:
                self.is_mute = False
                self.say('マイクはオンです')
                logger.info('mute off')

            res = {
                'isMute': detail['isMute']
            }
            return res

        if command == 'GET_VOLUME':
            mic, speaker = alsa.get_default()
            vol = alsa.get_current_volume(int(speaker['card_id']))
            return {
                'volume': vol
            }

        if command == 'SET_VOLUME':
            mic, speaker = alsa.get_default()
            alsa.set_current_volume(int(speaker['card_id']), int(detail['volume']))
            vol = alsa.get_current_volume(int(speaker['card_id']))
            return {
                'volume': vol
            }

        if command == 'GET_ASSISTANT_SETTING':
            setting = self.setting
            return {
                'setting': setting
            }

        if command == 'SET_ASSISTANT_SETTING':
            self.setting = detail['setting']
            return {}

        return None

    def stop(self):
        self.is_active=False

    def say(self,text):
        logger.warning('function say is dummy please implement this function')

    def conversation(self):
        logger.warning('function conversation is dummy please implement this function')


    def play_sound_onoff(self,is_on):
        if is_on:
            process.call('aplay %s' % self.on_sound_path)
        else:
            process.call('aplay %s' % self.off_sound_path)



