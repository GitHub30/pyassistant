from assistant.record.sox_recorder import SoxRecorder
from assistant.asr.cognitive_speech import CognitiveSpeech
from assistant.util.assistant import Assistant
from assistant.slu.cognitive_luis import CognitiveLuis
from assistant.tts.open_jtalk import OpenJtalk
from assistant.hwd.snowboy import Snowboy

import logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')
logger.setLevel(logging.INFO)

class PiAssistant(Assistant):
    def __init__(self):
        super().__init__()
        self.__is_active = True
        self.__is_mute = False

    def stop(self):
        self.__is_active = False

    def set_mute(self,mute):
        self.__is_mute = mute

    def get_mute(self):
        return self.__is_mute

    def is_active(self):
        return self.__is_active

    def conversation(self):
        self.hwd = Snowboy()
        self.recorder = SoxRecorder()
        self.asr = CognitiveSpeech(self.setting['COGNITIVE_SPEECH_KEY'])
        self.slu = CognitiveLuis(self.setting['COGNITIVE_LUIS_APPID'], self.setting['COGNITIVE_LUIS_APPKEY'])
        self.tts = OpenJtalk()
        while self.__is_active:
            yield ('CONVERSATION_START',None)
            hotword = self.hwd.start(lambda :self.__is_active,lambda :self.__is_mute)

            if hotword == None:
                continue
                
            yield ('DETECT_HOTWORD', hotword)
            file = self.recorder.record()
            yield ('USER_SPEECH_END',file)

            text = self.asr.recognize(file)
            yield ('ASR_END', text)

            if text == None:
                continue

            intent,entities = self.slu.understand(text)
            yield ('SLU_END',(intent,entities))

    def say(self,text):
        self.tts.say(text)
