import subprocess
import tempfile
import assistant.util.package as package

class OpenJtalk():
    def __init__(self):
        package.install('open_jtalk', 'sudo apt-get install -y open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 open-jtalk')
        self.hts_voice = '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'
        self.speech_rate = 1.0


    def say(self,text):
        temp = tempfile.NamedTemporaryFile()
        file_text = temp.name+'.txt'
        with open(file_text, 'w') as f:
            f.write(text + '\n')

        temp = tempfile.NamedTemporaryFile()
        file_audio = temp.name+'.wav'


        dic = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
        cmd = "open_jtalk -m %s -x %s -ow %s %s -r %f"\
              % (self.hts_voice,
                 dic,
                 file_audio,
                 file_text,
                 self.speech_rate
                 )

        subprocess.call(cmd.split(' '))

        # aplayで再生
        cmd = "aplay %s"%(file_audio)
        subprocess.call(cmd.split(' '))