import urllib.request as request
import json


class WeatherResult():
    def __init__(self,city,description):
        self.city = city
        self.description = description

    def get_city(self):
        return self.city

    def get_description(self):
        return self.description

    def __str__(self):
        return "<City:{},Description:{}>".format(self.city,self.description)

class LiveDoorWeather():
    def __init__(self):
        pass

    def current(self,cityid = 130010):
        # cityidはこのサイト(http://weather.livedoor.com/forecast/rss/primary_area.xml)から得られる
        # livedoorのAPIを用いて天気を検索する
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' % cityid
        req = request.Request(url)

        with request.urlopen(req) as res:
            result = res.read().decode('utf-8')
            result = json.loads(result)
        desc = result['description']['text'].split('\n')
        desc = ' '.join(desc[0:2])

        return WeatherResult(result['title'], desc)