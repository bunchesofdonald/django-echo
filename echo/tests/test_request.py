from echo.request import EchoRequest
from echo.tests import BaseEchoTestCase


class TestEchoRequest(BaseEchoTestCase):
    def test_launch_request_type(self):
        """EchoRequest should know when it's received a launch request"""
        expected = EchoRequest.LAUNCH_REQUEST
        http_request = self._generate_launch_request()
        request = EchoRequest(http_request)
        assert request.type == expected

    def test_session_ended_request_type(self):
        """EchoRequest should know when it's received a session ended request"""
        expected = EchoRequest.SESSION_ENDED_REQUEST
        http_request = self._generate_session_ended_request()
        request = EchoRequest(http_request)
        assert request.type == expected

    def test_intent_request_type(self):
        """EchoRequest should know when it's received an intent request"""
        expected = EchoRequest.INTENT_REQUEST
        http_request = self._generate_intent_request()
        request = EchoRequest(http_request)
        assert request.type == expected

    def test_returns_intent_data(self):
        """EchoRequest should be able to return the intent's data"""
        expected = self.intent_request['intent']
        http_request = self._generate_intent_request()
        request = EchoRequest(http_request)
        assert request.intent == expected

    def test_returns_session_attributes(self):
        """EchoRequest should be able to return the session attributes"""
        expected = {'key': 'value'}
        http_request = self._generate_intent_request(session=expected)
        request = EchoRequest(http_request)
        assert request.session == expected

    def test_can_update_session_attributes(self):
        """EchoRequest should allow you to update the session attributes"""
        expected = {'key': 'another_value'}
        http_request = self._generate_intent_request()
        request = EchoRequest(http_request)
        request.session.update(expected)
        assert request.session == expected
