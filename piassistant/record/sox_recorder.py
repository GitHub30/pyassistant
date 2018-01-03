import piassistant.util.package as package
import subprocess
import tempfile


class SoxRecorder():

    def __init__(self):
        package.install('sox', 'sudo apt-get install -y sox')
        self.threshold = '-35d'
        self.start_duration = '00:00:00.001'
        self.end_duration = '00:00:1'

    def record(self):
        temp = tempfile.NamedTemporaryFile()
        temp.close()
        file = temp.name+'.wav'
        cmd = 'sox -c 1 -r 16000 -d %s silence 1 % s -35d 1 % s -35d'% (file, self.start_duration,self.end_duration)
        subprocess.call(cmd.split(' '))
        return file