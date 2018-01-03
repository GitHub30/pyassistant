from assistant.record.sox_recorder import SoxRecorder
from assistant.asr.cognitive_speech import CognitiveSpeech
from assistant.util.assistant import Assistant


class PiAssistant(Assistant):
    def __init__(self):
        super().__init__()

    def start(self):
        recorder = SoxRecorder()
        file = recorder.record()

        asr = CognitiveSpeech(self.setting['COGNITIVE_SPEECH_KEY'])
        text = asr.recognize(file)
        print(text)

if __name__ == '__main__':
    with PiAssistant() as assistant:
        assistant.start()
