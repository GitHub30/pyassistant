import urllib.request as request
import urllib.parse as parse
import json


class BingSearch():
    def __init__(self,api_key):
        self.api_key =api_key
        if self.api_key == '':
            raise Exception('COGNITIVE_SEARCH_KEY is empty')

    def search_video(self,word,lang = 'ja-JP',count=35,videoLength='short'):
        word = parse.quote(word)
        url = 'https://api.cognitive.microsoft.com/bing/v7.0/videos/search?q={}'.format(word)
        url += '&mkt={}'.format(lang)
        url += '&count={}'.format(count)
        url += '&videoLength={}'.format(videoLength)

        req = request.Request(url)
        req.add_header('Ocp-Apim-Subscription-Key', self.api_key)
        with request.urlopen(req) as res:
            result = res.read().decode('utf-8')
            result = json.loads(result)

        return result