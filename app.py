# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import json
from assistant.app.piassistant import PiAssistant
import threading

import logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')
logger.setLevel(logging.INFO)

agent = None
agent_thread = None

clients = []

def start_assistant():
    global agent
    with PiAssistant() as agent:
        for event, content in agent.conversation():
            logger.info('------ [event] %s ------' % event)
            logger.info(content)
            if event == 'SLU_END':
                agent.say('こんにちは')
                agent.stop()


def process_command(command,detail):
    global agent
    global agent_thread

    if command == 'ASSISTANT_START':
        if agent.is_active():
            agent.stop()
        assistant_thread = threading.Thread(target=start_assistant)
        assistant_thread.start()
        agent.say('起動しました')

    if command == 'ASSISTANT_STOP':
        if agent.is_active():
            agent.stop()
        agent.say('終了しました')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("/static/index.html")



class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print('open')
        if self not in clients:
            clients.append(self)

    def on_message(self,msg):
        msg = json.loads(msg)
        process_command(msg.command,msg.detail)
        print(msg)

    def on_close(self):
        if self in clients:
            clients.remove(self)



if __name__ == '__main__':

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    app = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/ws', SocketHandler),
    ],**settings)
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()



