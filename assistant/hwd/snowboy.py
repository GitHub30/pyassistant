import os
import subprocess

dir_path = os.path.abspath(os.path.dirname(__file__))
target = os.path.join(dir_path,'snowboydetect.py')
resource = os.path.join(dir_path,'common.res')
setup = os.path.join(dir_path,'setup.sh')

if not os.path.exists(target):
    subprocess.call(setup)

import pyaudio
import time
import wave
import collections
from . import snowboydetect



class RingBuffer(object):
    """Ring buffer to hold audio from PortAudio"""

    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        """Adds data to the end of buffer"""
        self._buf.extend(data)

    def get(self):
        """Retrieves data from the beginning of buffer and clears it"""
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp

class Snowboy():

    def __init__(self, decoder_model = os.path.join(dir_path,'helloraspi.pmdl'),sensitivity=[],audio_gain=1):

        tm = type(decoder_model)
        ts = type(sensitivity)
        if tm is not list:
            decoder_model = [decoder_model]
        if ts is not list:
            sensitivity = [sensitivity]
        model_str = ",".join(decoder_model)

        self.detector = snowboydetect.SnowboyDetect(resource.encode(),model_str.encode())
        self.detector.SetAudioGain(audio_gain)
        self.num_hotwords = self.detector.NumHotwords()

        if len(decoder_model) > 1 and len(sensitivity) == 1:
            sensitivity = sensitivity * self.num_hotwords
        if len(sensitivity) != 0:
            assert self.num_hotwords == len(sensitivity), \
                "number of hotwords in decoder_model (%d) and sensitivity " \
                "(%d) does not match" % (self.num_hotwords, len(sensitivity))
        sensitivity_str = ",".join([str(t) for t in sensitivity])
        if len(sensitivity) != 0:
            self.detector.SetSensitivity(sensitivity_str.encode())

        self.ring_buffer = RingBuffer(self.detector.NumChannels() * self.detector.SampleRate() * 5)


    def start(self,sleep_time=0.03):

        def audio_callback(in_data, frame_count, time_info, status):
            self.ring_buffer.extend(in_data)
            play_data = chr(0) * len(in_data)
            return play_data, pyaudio.paContinue

        self.audio = pyaudio.PyAudio()
        self.stream_in = self.audio.open(
            input=True, output=False,
            format=self.audio.get_format_from_width(
                self.detector.BitsPerSample() / 8),
            channels=self.detector.NumChannels(),
            rate=self.detector.SampleRate(),
            frames_per_buffer=2048,
            stream_callback=audio_callback)

        self.hotword = None

        while True:
            data = self.ring_buffer.get()
            if len(data) == 0:
                time.sleep(sleep_time)

            ans = self.detector.RunDetection(data)
            if ans == -1:
                raise("Error initializing streams or reading audio data")
                break
            elif ans > 0:
                self.hotword = ans
                break

        self.stream_in.stop_stream()
        self.stream_in.close()
        self.audio.terminate()

        return self.hotword
