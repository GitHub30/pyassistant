# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import json
from assistant.app.piassistant import PiAssistant
import threading
import click

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

        print('restart')
    if command == 'ASSISTANT_MUTE_START':

        if agent != None and agent.is_active():
            agent.set_mute(True)
            agent.say('マイクはオフです')
            print('mute on')

    if command == 'ASSISTANT_MUTE_STOP':

        if agent != None and agent.is_active():
            agent.set_mute(False)
            agent.say('マイクはオンです')
            print('mute off')


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
        process_command(msg['command'],msg['detail'])


    def on_close(self):
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
            logger.error(e.args)
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



