import urllib.request as request
import urllib.parse as parse
import uuid
import json


class CognitiveSpeech():

    def __init__(self,key):
        self.key = key
        if self.key == '':
            raise Exception('COGNITIVE_SPEECH_KEY is empty')

    def recognize(self,file):
        url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
        req = request.Request(url)
        req.add_header('Ocp-Apim-Subscription-Key', self.key)
        with request.urlopen(req, data=''.encode('utf-8')) as res:
            token = res.read().decode("utf-8")

        with open(file, 'rb') as f:
            audio = f.read()

        url = 'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1'
        url += '?Version=3.0'
        url += '&language=ja-JP'
        url += '&format=json'
        url += '&requestid=' + str(uuid.uuid4())

        req = request.Request(url)
        req.add_header('Authorization', 'Bearser ' + token)
        req.add_header('Content-Type', 'audio/wav; codec="audio/pcm"; samplerate=16000')
        with request.urlopen(req, data=audio) as res:
            result = res.read().decode('utf-8')
            print(result)
        result = json.loads(result)

        if 'DisplayText' in result:
            text = result['DisplayText']
        else:
            text = None
        return text