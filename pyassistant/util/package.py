import subprocess
import logging
logger = logging.getLogger('pyassistant')

def install(command,init):
    try:
        proc = subprocess.Popen(command.split(' '),stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        res = proc.communicate()
    except FileNotFoundError:
        logger.info('package %s is not found'%command)
        logger.info('install %s'%init)
        subprocess.call(init.split(' '))

    try:
        proc = subprocess.Popen(command.split(' '), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        res = proc.communicate()
    except FileNotFoundError:
        logger.error('command %s could not installed by this command %s'%(command,init))
