# -*- coding: utf-8 -*-
import logging
import click
from pyassistant.app.assistant_base import AssistantBase
from pyassistant.asr.cognitive_speech import CognitiveSpeech
from pyassistant.record.sox_recorder import SoxRecorder
from pyassistant.slu.cognitive_luis import CognitiveLuis
from pyassistant.trigger.button_trigger import ButtonTrigger
from pyassistant.trigger.snowboy import Snowboy
from pyassistant.tts.open_jtalk import OpenJtalk
from pyassistant.ir.ir_controller import IRController
from pyassistant.weather.livedoor import LiveDoorWeather
import pyassistant.util.alsa as alsa
from pyassistant.music.youtube_dj import YoutubeDj

logging.basicConfig()
logger = logging.getLogger('pyassistant')
logger.setLevel(logging.INFO)

class PyAssistant(AssistantBase):
    def __init__(self):
        super().__init__()
        self.tts = OpenJtalk()

        self.ir = IRController(self.setting['IR_SCAN_GPIO'],self.config_dir)
        self.music = YoutubeDj(self.setting['COGNITIVE_SEARCH_KEY'])
        self.weather = LiveDoorWeather()
        alsa.set_default(
            mic_card_id=self.setting['MIC_CARD_ID'],
            mic_device_id=self.setting['MIC_DEVICE_ID'],
            speaker_card_id=self.setting['SPEAKER_CARD_ID'],
            speaker_device_id=self.setting['SPEAKER_DEVICE_ID']
        )

    def conversation(self):

        yield ('CONVERSATION_START', None)

        while self.is_active:
            yield ('TURN_START', None)
            yield ('WAIT_TRIGGER', None)
            if self.setting['ACTIVATION_TRIGGER'] =='snowboy':
                trigger = Snowboy()
                is_detect = trigger.start(lambda :self.is_active,lambda :self.is_mute)
            elif self.setting['ACTIVATION_TRIGGER'] =='button':
                trigger = ButtonTrigger(int(self.setting['TRIGGER_GPIO']))
                is_detect = trigger.start(lambda :self.is_active)

            yield ('DETECT_TRIGGER',is_detect)
            if is_detect:
                self.play_sound_onoff(is_on=True)

                yield ('USER_SPEECH_START',None)
                recorder = SoxRecorder()
                recorder.threshold = self.setting['RECORD_THRESHOLD']
                recorder.start_second = self.setting['RECORD_BEGIN_SECOND']
                recorder.end_seond = self.setting['RECORD_END_SECOND']
                file = recorder.record()
                yield ('USER_SPEECH_END',file)
                self.play_sound_onoff(is_on=False)
                yield ('ASR_START',None)
                asr = CognitiveSpeech(self.setting['COGNITIVE_SPEECH_KEY'])
                asr_text = asr.recognize(file)
                yield ('ASR_FINISH', asr_text)

                if asr_text:
                    yield ('SLU_START', None)
                    slu = CognitiveLuis(
                        self.setting['COGNITIVE_LUIS_APPID'],
                        self.setting['COGNITIVE_LUIS_APPKEY']
                    )

                    result = slu.understand(asr_text)
                    yield ('SLU_FINISH',result)
            else:
                raise Exception('Error in pyassistant')

            yield ('TURN_FINISH', None)

        yield ('CONVERSATION_FINISH', None)

    def say(self,text):
        self.tts.say(text)



@click.group(help='PyAssistant App',invoke_without_command=True)
@click.option('--debug/--no-debug',default=False,help='enable debug mode if set 1')
@click.pass_context
def __main(ctx,debug):
    if debug:
        logger.setLevel(logging.DEBUG)

@__main.group(help='IR mode')
@click.pass_context
def ir(ctx):
    pass

@ir.command('register',help='')
@click.option('-n','--name','name',type=str,help='',required=True)
@click.option('-p','--pin','pin',type=str,help='',required=True)
@click.pass_context
def ir_register(ctx,name,pin):

    with PyAssistant() as agent:
        logger.info('IR receive module connected GPIO %d'%agent.ir.scan_pin)
        input('send ir to IR receive module when after type any key:')

        result = agent.ir.register_channel(name,send_pin=int(pin))
        if result:
            logger.info('registration complete!')

            logger.info('\n----------- all IR channels -----------\n')
            for name,value in agent.ir.list_channels().items():
                logger.info('name = [%s] GPIO = [%d]'%(name,value['pin']))

            logger.info('\n---------------------------------------\n')
        else:
            logger.error('registration faild! please retry')


@ir.command('unregister',help='')
@click.option('-n','--name','name',type=str,help='',required=True)
@click.pass_context
def ir_unregister(ctx,name):
    with PyAssistant() as agent:
        result = agent.ir.unregister_channel(name)
        if result:
            logger.info('unregister complete!')
            logger.info('\n----------- all IR channels -----------\n')
            for name, value in agent.ir.list_channels().items():
                logger.info('name = [%s] GPIO = [%d]' % (name, value['pin']))

            logger.info('\n---------------------------------------\n')
        else:
            logger.error('unregistration faild!')


@ir.command('list',help='')
@click.pass_context
def ir_list(ctx):
    with PyAssistant() as agent:
        logger.info('\n----------- all IR channels -----------\n')
        for name, value in agent.ir.list_channels().items():
            logger.info('name = [%s] GPIO = [%d]' % (name, value['pin']))

        logger.info('\n---------------------------------------\n')


@ir.command('send',help='')
@click.option('-n','--name','name',type=str,help='',required=True)
@click.option('-r','--repeat','repeat',type=str,help='',default=3,required=False)
@click.pass_context
def ir_send(ctx,name,repeat):
    with PyAssistant() as agent:
        agent.ir.send_channel(name,send_repeat=repeat)


@__main.group(help='Assistant mode')
@click.pass_context
def assistant(ctx):
    pass

@assistant.command('run',help='')
@click.pass_context
def run_assistant(ctx):
    with PyAssistant() as agent:
        while True:
            for event, result in agent.conversation():
                logger.info('------ [event] %s ------' % event)
                logger.info(result)
                if event == 'SLU_FINISH':
                    if result.get_intent() == 'greeting':
                        agent.say('こんにちは。今日もいい天気ですね')
                    if result.get_intent() == 'weather':
                        agent.say('天気をお調べします')
                        wr = agent.weather.current(cityid = 130010)
                        agent.say('%sの天気は%sです'%(wr.get_city(),wr.get_description()))

                    if result.get_intent() == 'tv_on':
                        agent.say('テレビをオンにします')
                        agent.ir.send_channel('tv_on')
                    if result.get_intent() == 'tv_off':
                        agent.say('テレビをオフにします')
                        agent.ir.send_channel('tv_off')

                    if result.get_intent() == 'play_music':
                        if len(result.get_entities()) == 0:
                            keyword = '音楽'
                        else:
                            keyword = result.get_entities()[0]
                        agent.say(keyword+' についてのミュージックを再生します')
                        agent.music.play(keyword)
                    if result.get_intent() == 'next_music':
                        agent.music.next()
                    if result.get_intent() == 'stop_music':
                        agent.music.stop()

if __name__ == '__main__':
    __main()



