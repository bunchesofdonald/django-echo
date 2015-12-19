import logging
import json

from django import http


log = logging.getLogger(__name__)


class EchoResponse(http.HttpResponse):
    PLAIN_TEXT_OUTPUT = 'PlainText'

    def __init__(self, text, output_type, session, end_session, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json;charset=UTF-8')

        response_body = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": output_type,
                    "text": text
                },
                "card": None,
                "reprompt": None,
                "shouldEndSession": end_session
            },
            "sessionAttributes": session
        }

        log.debug(response_body)
        data = json.dumps(response_body)
        super(EchoResponse, self).__init__(content=data, **kwargs)


class EchoSimplePlainTextResponse(EchoResponse):
    def __init__(self, text, session=None, end_session=True, *args, **kwargs):
        if session is None:
            session = {}

        super(EchoSimplePlainTextResponse, self).__init__(
            text=text,
            output_type=EchoResponse.PLAIN_TEXT_OUTPUT,
            end_session=end_session,
            session=session,
            **kwargs
        )
