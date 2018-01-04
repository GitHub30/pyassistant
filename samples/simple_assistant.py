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

    def conversation(self):
        self.hwd = Snowboy()
        self.recorder = SoxRecorder()
        self.asr = CognitiveSpeech(self.setting['COGNITIVE_SPEECH_KEY'])
        self.slu = CognitiveLuis(self.setting['COGNITIVE_LUIS_APPID'], self.setting['COGNITIVE_LUIS_APPKEY'])
        self.tts = OpenJtalk()
        while True:
            yield ('CONVERSATION_START',None)
            hotword = self.hwd.start()
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

if __name__ == '__main__':
    with PiAssistant() as assistant:
        for event,content in assistant.conversation():
            logger.info('------ [event] %s ------'%event)
            logger.info(content)
            if event == 'SLU_END':
                assistant.say('こんにちは')

