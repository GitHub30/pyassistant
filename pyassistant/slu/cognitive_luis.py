from luis_sdk import LUISClient
import logging
logging.basicConfig()
logger = logging.getLogger('pyassistant')


class LuisResult():
    def __init__(self,intent,entities):
        self.intent = intent
        self.entities= entities

    def get_intent(self):
        return self.intent

    def get_entities(self):
        return self.entities

    def __str__(self):
        return "<Intent:{},Entities:[{}]>".format(self.intent,','.join(self.entities))


class CognitiveLuis():
    def __init__(self,appid,appkey):
        self.appid = appid
        self.appkey = appkey

        if self.appid == '':
            logger.warning('COGNITIVE_LUIS_APPID is empty')
        if self.appkey == '':
            logger.warning('COGNITIVE_LUIS_APPKEY is empty')

    def understand(self,text):
        client = LUISClient(self.appid, self.appkey, True)
        res = client.predict(text)
        top = res.get_top_intent()
        entities = res.get_entities()
        entities = [(x.get_type(), x.get_name()) for x in entities]
        intent = top.get_name()
        result = LuisResult(intent, entities)
        return result
