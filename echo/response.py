import logging
import json

from django import http


log = logging.getLogger(__name__)

PLAIN_TEXT_OUTPUT = 'PlainText'


class EchoResponse(http.HttpResponse):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json;charset=UTF-8')

        response_body = {
            "version": "1.0",
            "response": {
                "outputSpeech": kwargs.pop('output_speech'),
                "card": kwargs.pop('card', None),
                "reprompt": kwargs.pop('reprompt', None),
                "shouldEndSession": kwargs.pop('should_end_session', True)
            },
            "sessionAttributes": kwargs.pop('session', {})
        }

        log.debug(response_body)
        data = json.dumps(response_body)
        super(EchoResponse, self).__init__(content=data, **kwargs)


class EchoTextResponse(EchoResponse):
    def __init__(self, text, session=None, should_end_session=True, *args, **kwargs):
        output_speech = {"type": PLAIN_TEXT_OUTPUT, "text": text}

        super(EchoTextResponse, self).__init__(
            output_speech=output_speech,
            should_end_session=should_end_session,
            session=session,
            **kwargs
        )
