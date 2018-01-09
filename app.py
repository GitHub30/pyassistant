# -*- coding: utf-8 -*-
import logging
import click
from pyassistant.app.pyassistant import PyAssistant

logging.basicConfig()
logger = logging.getLogger('pi-pyassistant')
logger.setLevel(logging.INFO)

@click.command()
@click.option('--debug','-d',default=0,type=int,help='enable debug mode if set 1')
def __main(debug):
    if debug >0:
        logger.setLevel(logging.DEBUG)

    with PiAssistant() as agent:
        while True:
            for event, content in agent.conversation():
                logger.info('------ [event] %s ------' % event)
                logger.info(content)



if __name__ == '__main__':
    __main()



