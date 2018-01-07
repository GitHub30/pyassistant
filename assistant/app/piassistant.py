from assistant.record.sox_recorder import SoxRecorder
from assistant.asr.cognitive_speech import CognitiveSpeech
from assistant.util.assistant import Assistant
from assistant.slu.cognitive_luis import CognitiveLuis
from assistant.tts.open_jtalk import OpenJtalk
from assistant.trigger.snowboy import Snowboy
from assistant.trigger.button_trigger import ButtonTrigger

import logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')
logger.setLevel(logging.INFO)

class PiAssistant(Assistant):
    def __init__(self):
        super().__init__()
        self.__is_active = True
        self.__is_mute = False
        self.tts = OpenJtalk()

    def stop(self):
        self.__is_active = False

    def set_mute(self,mute):
        self.__is_mute = mute

    def get_mute(self):
        return self.__is_mute

    def is_active(self):
        return self.__is_active

    def set_setting(self,setting):
        self.setting = setting

    def get_setting(self):
        return self.setting

    def conversation(self):
        while self.__is_active:
            yield ('CONVERSATION_START',None)
            if self.setting['ACTIVATION_TRIGGER']['value']['value'] =='snowboy':
                self.trigger = Snowboy()
                isDetect = self.trigger.start(lambda :self.__is_active,lambda :self.__is_mute)
            elif self.setting['ACTIVATION_TRIGGER']['value']['value'] =='button':
                self.trigger = ButtonTrigger(int(self.setting['TRIGGER_GPIO']['value']['value']))
                isDetect = self.trigger.start(lambda :self.__is_active)

            if isDetect == False:
                continue

            yield ('DETECT_HOTWORD', self.trigger)
            self.recorder = SoxRecorder()
            self.recorder.threshold = self.setting['RECORD_THRESHOLD']['value']
            self.recorder.start_second = self.setting['RECORD_BEGIN_SECOND']['value']
            self.recorder.end_seond = self.setting['RECORD_END_SECOND']['value']
            file = self.recorder.record()
            yield ('USER_SPEECH_END',file)
            self.asr = CognitiveSpeech(self.setting['COGNITIVE_SPEECH_KEY']['value'])
            text = self.asr.recognize(file)
            yield ('ASR_END', text)

            if text == None:
                continue
            self.slu = CognitiveLuis(self.setting['COGNITIVE_LUIS_APPID']['value'],
                                     self.setting['COGNITIVE_LUIS_APPKEY']['value'])

            intent,entities = self.slu.understand(text)
            yield ('SLU_END',(intent,entities))

    def say(self,text):
        self.tts.say(text)
