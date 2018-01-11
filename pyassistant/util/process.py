import subprocess
import logging
logging.basicConfig()
logger = logging.getLogger('pyassistant')


def call(command):
    logger.debug(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = p.stdout.read().decode('utf-8')
    stderr = p.stderr.read().decode('utf-8')
    for o in stdout.split('\n'):
        logger.debug(o)

    for o in stderr.split('\n'):
        logger.debug(o)

