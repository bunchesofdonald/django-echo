import json

from django.test import TestCase, RequestFactory


class BaseEchoTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.base_request_data = {
            "session": {
                "sessionId": "SessionId.123",
                "application": {
                    "applicationId": "amzn1.echo-sdk-ams.app.123"
                },
                "attributes": None,
                "user": {
                    "userId": "amzn1.echo-sdk-account.123"
                },
                "new": False
            },
            "request": None
        }

        self.base_response_data = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": ""
                },
                "card": None,
                "reprompt": None,
                "shouldEndSession": False
            },
            "sessionAttributes": {}
        }

        self.launch_request = {
            "type": "LaunchRequest",
            "requestId": "EdwRequestId.123",
            "timestamp": 1450024241777,
        }

        self.session_ended_request = {
            "type": "SessionEndedRequest",
            "requestId": "EdwRequestId.123",
            "timestamp": 1450024241777,
            "reason": "USER_INITIATED"
        }

        self.intent_request = {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.123",
            "timestamp": 1450024241777,
            "intent": {
                "name": "TheIntent",
                "slots": {}
            }
        }

    def _generate_request(self, request_data):
        http_request = self.factory.post('/')
        http_request._body = json.dumps(request_data)
        return http_request

    def _generate_launch_request(self):
        request_data = self.base_request_data
        request_data['request'] = self.launch_request
        return self._generate_request(request_data)

    def _generate_session_ended_request(self):
        request_data = self.base_request_data
        request_data['request'] = self.session_ended_request
        return self._generate_request(request_data)

    def _generate_intent_request(self, intent_name="TheIntent", slots=None, session=None):
        request_data = self.base_request_data
        request_data['request'] = self.intent_request
        request_data['request']['intent']['name'] = intent_name

        if slots:
            request_data['request']['intent']['slots'] = slots

        if session:
            request_data['session']['attributes'] = session

        return self._generate_request(request_data)
