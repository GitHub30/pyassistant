from pyassistant.search.bing_search import BingSearch
from pyassistant.music.youtube import YoutubePlayer
import random
import os
import json

class YoutubeDj():

    def __init__(self,bing_apikey):
        self.player = YoutubePlayer()
        self.search = BingSearch(bing_apikey)
        self.current_index = 0
        self.current_music = None
        with open(os.path.join(os.path.dirname(__file__),'sources.json'),'r') as f:
            self.sources = json.load(f)


    def play(self,keyword=None,lang='ja-JP'):
        if not keyword:
            keywords = [x['keyword'] for x in self.sources['lang'][lang]]
            random.shuffle(keywords)
            keyword = keywords[0]
        query = '"{}" "{}"'.format(keyword,'Music Video')
        self.play_list = self.search.search_video(query,lang,count=50)
        self.play_list = [(x['name'],x['contentUrl']) for x in self.play_list['value'] if x['contentUrl'].count('youtube.com') > 0]
        random.shuffle(self.play_list)
        self.current_index = 0
        self.current_music = self.play_list[self.current_index]
        if self.player.is_playing:
            self.player.stop()
        self.player.play(self.current_music[1],self.__finish_current)


    def next(self):
        if self.current_index+1<len(self.play_list):
            self.current_index+=1
            self.current_music = self.play_list[self.current_index]
            if self.player.is_playing:
                self.player.stop()
            self.player.play(self.current_music[1],self.__finish_current)

    def prev(self):
        if self.current_index-1>-1:
            self.current_index-=1
            self.current_music = self.play_list[self.current_index]
            if self.player.is_playing:
                self.player.stop()
            self.player.play(self.current_music[1],self.__finish_current)

    def get_current(self):
        return self.current_music


    def __finish_current(self,is_manual_stop):
        if not is_manual_stop:
            self.next()
            print('stop')



if __name__ == '__main__':
    dj = YoutubeDj('')
    dj.play()
    while True:
        print('please input command')
        command = input()
        if command == 'next':
            dj.next()
        if command == 'prev':
            dj.prev()
        if command == 'stop':
            dj.player.stop()

        print(dj.current_music[0])