import json

import mock

from django.test import TestCase, RequestFactory

from echo.skill import (
    LAUNCH_NOT_IMPLEMENTED_ERROR,
    SESSION_ENDED_NOT_IMPLEMENTED_ERROR,
    EchoSkill,
)


class TestEchoSkill(TestCase):
    def setUp(self):
        self.skill = EchoSkill()

        self.factory = RequestFactory()
        self.http_request = self.factory.post('/')

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

    def test_routes_to_launch(self):
        """A LaunchRequest should raise a NotImplementedError"""
        expected = (NotImplementedError, LAUNCH_NOT_IMPLEMENTED_ERROR)

        request_data = self.base_request_data
        request_data['request'] = self.launch_request
        self.http_request._body = json.dumps(request_data)

        with self.assertRaisesMessage(*expected):
            self.skill.dispatch(self.http_request)

    def test_routes_to_session_ended(self):
        """A SessionEndedRequest should raise a NotImplementedError"""
        expected = (NotImplementedError, SESSION_ENDED_NOT_IMPLEMENTED_ERROR)

        request_data = self.base_request_data
        request_data['request'] = self.session_ended_request
        self.http_request._body = json.dumps(request_data)

        with self.assertRaisesMessage(*expected):
            self.skill.dispatch(self.http_request)

    def test_get_intent_handler_name(self):
        """get_intent_handler_name should know how to un-camelcase a string"""
        expected = "this_is_a_camel_cased_string"
        assert self.skill.get_intent_handler_name("ThisIsACamelCasedString") == expected

    def test_routes_to_intent(self):
        """A IntentRequest should be routed to the proper intent handler"""
        expected = 1

        request_data = self.base_request_data
        request_data['request'] = self.intent_request
        self.http_request._body = json.dumps(request_data)

        self.skill.the_intent = None
        with mock.patch.object(self.skill, 'the_intent') as mock_intent:
            self.skill.dispatch(self.http_request)
            assert mock_intent.call_count == expected

    def test_routes_to_intent_with_session_and_slot_data(self):
        """A IntentRequest should be routed to the proper intent handler with session and slot data"""
        expected = {
            'slots': {
                'Sign': {
                    'name': 'Sign',
                    'value': 'Virgo'
                }
            },
            'session': {
                'saved_value': 123
            }
        }

        request_data = self.base_request_data
        request_data['request'] = self.intent_request
        request_data['request']['intent']['slots'] = expected['slots']
        request_data['session']['attributes'] = expected['session']

        self.http_request._body = json.dumps(request_data)

        self.skill.the_intent = None
        with mock.patch.object(self.skill, 'the_intent') as mock_intent:
            self.skill.dispatch(self.http_request)
            mock_intent.assert_called_once_with(**expected)
