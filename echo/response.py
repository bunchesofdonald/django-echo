import json

from django import http


class EchoSimplePlainTextResponse(http.HttpResponse):
    def __init__(self, text, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json;charset=UTF-8')

        response_body = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": text
                },
                "card": None,
                "reprompt": None,
                "shouldEndSession": True
            },
            "sessionAttributes": None
        }

        data = json.dumps(response_body)
        super(EchoSimplePlainTextResponse, self).__init__(content=data, **kwargs)
