import subprocess
import threading
import signal
import os
import sys
import time

class YoutubePlayer():

    def __init__(self):
        self.process_dl = None
        self.process_play = None
        self.chunksize = 5
        self.player_thread = None
        self.is_playing = False
        self.is_pausing = False
        self.is_pausing_first = True

    def __play_async(self,url,finish_callback):
        cmd_dl = 'youtube-dl "%s" -f "bestaudio" -o -' % url
        self.process_dl = subprocess.Popen(cmd_dl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_play = 'mplayer -'
        devnull = open('/dev/null', 'w')
        self.process_play = subprocess.Popen(cmd_play, shell=True,stdin=subprocess.PIPE, stdout=devnull, stderr=sys.stderr)

        is_manual_stop = False
        while True:
            try:
                if not self.is_pausing:
                    d = self.process_dl.stdout.read(self.chunksize)
                    self.process_play.stdin.write(d)
                    if d == b'':
                        is_manual_stop = False
                        break
                else:
                    if self.is_pausing_first:
                        self.process_play.send_signal(signal.SIGSTOP)
                        self.process_dl.send_signal(signal.SIGSTOP)
                        self.is_pausing_first = False
                    time.sleep(0.1)
            except:
                is_manual_stop = True
                break

        self.is_playing = False
        finish_callback(is_manual_stop)

    def play(self,url,finish_callback):
        self.is_playing = True
        self.is_pausing = False
        self.player_thread = threading.Thread(target=self.__play_async,args=(url,finish_callback))
        self.player_thread.start()


    def pause(self):
        self.is_pausing = True
        self.is_pausing_first = True
        self.is_playing = False

    def resume(self):
        self.process_dl.send_signal(signal.SIGCONT)
        self.process_play.send_signal(signal.SIGCONT)
        self.is_pausing = False
        self.is_playing = True

    def stop(self):
        self.is_pausing = False
        self.process_play.kill()
        self.process_dl.kill()
        self.process_play = None
        self.process_dl = None
        self.player_thread.join()

if __name__ == '__main__':

    def c(is_manual):
        print('end')
        pass
    player = YoutubePlayer()
    while True:
        print('please input command')
        command = input()
        if command == 'play':
            player.play("https://youtu.be/4EW-9VH_iZI",c)
        if command == 'pause':
            player.pause()
        if command == 'resume':
            player.resume()
        if command == 'stop':
            player.stop()
