import json

from echo.response import (
    PLAIN_TEXT_OUTPUT,
    EchoTextResponse,
)
from echo.tests import BaseEchoTestCase


class TestEchoSimplePlainTextResponse(BaseEchoTestCase):
    def test_populates_text_in_response(self):
        """The Plain text response should populate the outputSpeech"""
        expected = "This is the text"
        response = EchoTextResponse(expected)
        data = json.loads(response.content.decode())

        assert data['response']['outputSpeech']['type'] == PLAIN_TEXT_OUTPUT
        assert data['response']['outputSpeech']['text'] == expected

    def test_populates_session(self):
        """The Plain text response should populate the session attributes"""
        expected = {'apple': 'red', 'orange': 'orange'}
        response = EchoTextResponse('text', session=expected)
        data = json.loads(response.content.decode())

        assert data['sessionAttributes'] == expected

    def test_sets_end_session_bool(self):
        """The Plain text response should be able to set the shouldEndSession bool"""
        response = EchoTextResponse('text', should_end_session=False)
        data = json.loads(response.content.decode())
        assert not data['response']['shouldEndSession']
