import logging
import json

from django import http


log = logging.getLogger(__name__)

PLAIN_TEXT_OUTPUT_TYPE = 'PlainText'
SSML_OUTPUT_TYPE = 'SSML'

SIMPLE_CARD = 'Simple'
LINK_ACCOUNT_CARD = 'LinkAccount'


def create_simple_card(title, content):
    return {
        "type": SIMPLE_CARD,
        "title": title,
        "content": content,
    }


def create_link_account_card():
    return {"type": LINK_ACCOUNT_CARD, }


class EchoResponse(http.HttpResponse):
    def __init__(self, output_speech, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json;charset=UTF-8')

        reprompt = kwargs.pop('reprompt', None)
        if reprompt:
            reprompt = self.get_speech_object(reprompt)

        response_body = {
            "version": "1.0",
            "response": {
                "outputSpeech": self.get_speech_object(output_speech),
                "card": kwargs.pop('card', None),
                "reprompt": reprompt,
                "shouldEndSession": kwargs.pop('should_end_session', True)
            },
            "sessionAttributes": kwargs.pop('session', {})
        }

        log.debug(response_body)
        data = json.dumps(response_body)
        super(EchoResponse, self).__init__(content=data, **kwargs)

    def is_ssml(self, text):
        text = text.strip()
        return text.startswith('<speak>') and text.endswith('</speak>')

    def get_speech_object(self, text):
        if self.is_ssml(text):
            return {
                "type": SSML_OUTPUT_TYPE,
                "ssml": text
            }
        else:
            return {
                "type": PLAIN_TEXT_OUTPUT_TYPE,
                "text": text
            }
