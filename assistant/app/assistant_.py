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
            self.first_launch = False
        else:
            self.setting = {}
            self.first_launch = True

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



