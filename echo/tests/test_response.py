import json

from echo.response import EchoResponse, EchoSimplePlainTextResponse
from echo.tests import BaseEchoTestCase


class TestEchoSimplePlainTextResponse(BaseEchoTestCase):
    def test_populates_text_in_response(self):
        """The Plain text response should populate the outputSpeech"""
        expected = "This is the text"
        response = EchoSimplePlainTextResponse(expected)
        data = json.loads(response.content.decode())

        assert data['response']['outputSpeech']['type'] == EchoResponse.PLAIN_TEXT_OUTPUT
        assert data['response']['outputSpeech']['text'] == expected

    def test_populates_session(self):
        """The Plain text response should populate the session attributes"""
        expected = {'apple': 'red', 'orange': 'orange'}
        response = EchoSimplePlainTextResponse('text', session=expected)
        data = json.loads(response.content.decode())

        assert data['sessionAttributes'] == expected

    def test_sets_end_session_bool(self):
        """The Plain text response should be able to set the end_session bool"""
        response = EchoSimplePlainTextResponse('text', end_session=False)
        data = json.loads(response.content.decode())
        assert not data['response']['shouldEndSession']
