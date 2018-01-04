import assistant.util.package as package
import subprocess
import tempfile
import assistant.util.alsa as alsa

class SoxRecorder():

    def __init__(self):
        package.install('sox', 'sudo apt-get install -y sox')
        self.threshold = '-15d'
        self.start_duration = '00:00:00.3'
        self.end_duration = '00:00:1'
        self.default_mic,self.default_speaker = alsa.get_default()

    def record(self):
        temp = tempfile.NamedTemporaryFile()
        temp.close()
        file = temp.name+'.wav'
        cmd = 'sox -c 1 -t alsa plughw:%s,%s %s silence 1 % s -35d 1 % s -35d'% (self.default_mic['card_id'],self.default_mic['device_id'],file, self.start_duration,self.end_duration)
        subprocess.call(cmd.split(' '))
        return file