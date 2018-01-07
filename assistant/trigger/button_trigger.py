import os
import subprocess
import RPi.GPIO as GPIO
import time
import logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')



class ButtonTrigger():

    def __init__(self,trigger_pin):
        self.trigger_pin = trigger_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.trigger_event = False

    def __on_event(self,arg):
        self.trigger_event = True

    def start(self,stop_callback):
        logger.info('waiting for GPIO %d rising...'%self.trigger_pin)
        GPIO.add_event_detect(self.trigger_pin,GPIO.RISING,self.__on_event)
        while stop_callback():
            if self.trigger_event:
                break

            time.sleep(0.1)

        GPIO.remove_event_detect(self.trigger_pin)
        GPIO.cleanup(self.trigger_pin)
        return self.trigger_event


