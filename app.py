# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import json
from assistant.app.piassistant import PiAssistant
import threading
import click
import assistant.util.alsa as alsa
import traceback

import logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')
logger.setLevel(logging.INFO)

agent = None
agent_thread = None

clients = []



def process_command(command,detail):
    global agent
    global agent_thread

    if command == 'ASSISTANT_RESTART':
        agent.say('再起動します')
        if agent != None and agent.is_active():
            agent.stop()
        return {}
    if command == 'ASSISTANT_MUTE':
        if detail['isMute']:
            agent.set_mute(True)
            agent.say('マイクはオフです')
            logger.info('mute on')
        else:
            agent.set_mute(False)
            agent.say('マイクはオンです')
            logger.info('mute off')

        res =  {
            'isMute':detail['isMute']
        }
        return res

    if command == 'GET_VOLUME':
        mic,speaker = alsa.get_default()
        vol = alsa.get_current_volume(int(speaker['card_id']))
        return {
            'volume':vol
        }

    if command == 'SET_VOLUME':
        mic, speaker = alsa.get_default()
        alsa.set_current_volume(int(speaker['card_id']),int(detail['volume']))
        vol = alsa.get_current_volume(int(speaker['card_id']))
        return {
            'volume':vol
        }

    if command == 'GET_ASSISTANT_SETTING':
        setting = agent.setting
        return {
            'setting':setting
        }

    if command == 'SET_ASSISTANT_SETTING':
        agent.setting = detail['setting']
        return {}

    return None




class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")



class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print('open')
        if self not in clients:
            clients.append(self)

    def on_message(self,msg):
        print(msg)
        msg = json.loads(msg)
        try:
            res = process_command(msg['command'],msg['detail'])

            if res != None:
                res_msg = {
                    'command':msg['command'],
                    'detail':res
                }
                self.write_message(json.dumps(res_msg))
        except Exception as e:
            res_msg = {
                'command': 'ASSISTANT_ERROR',
                'detail': {
                    'message':e.args
                }
            }
            self.write_message(json.dumps(res_msg))
            logger.error(e.args[0])
            logger.error(traceback.format_exc())

    def on_close(self):
        print('close')
        if self in clients:
            clients.remove(self)


def start_assistant():
    global agent

    while True:
        try:
            agent = PiAssistant()
            for event, content in agent.conversation():
                logger.info('------ [event] %s ------' % event)
                logger.info(content)
                if event == 'SLU_END':
                    agent.say('こんにちは')
        except Exception as e:
            logger.error('Assistant raises following error!')
            logger.error(e.args[0])
            logger.error(traceback.format_exc())
            break


@click.command()
@click.option('--port','-p',default=8000)
def __main(port):
    option = {
    }
    assistant_thread = threading.Thread(target=start_assistant,kwargs=option)
    assistant_thread.start()

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    app = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/ws', SocketHandler),
    ], **settings)
    app.listen(port)
    logger.info('Assistant webUI listening at port %d'%port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    try:
        __main()
    except KeyboardInterrupt:
        logger.info('finish')



