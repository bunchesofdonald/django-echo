import json

from echo.response import (
    EchoResponse,
    EchoSSMLResponse,
    EchoTextResponse,
    OUTPUT_SPEECH_REQUIRED_ERROR,
    PLAIN_TEXT_OUTPUT,
    SIMPLE_CARD,
    SSML_OUTPUT,
)
from echo.tests import BaseEchoTestCase


class TestEchoResponse(BaseEchoTestCase):
    def setUp(self):
        super(TestEchoResponse, self).setUp()
        self.output_speech = {"type": PLAIN_TEXT_OUTPUT, "text": "text"}

    def test_output_speech_is_required(self):
        """EchoResponse should require output_speech parameter"""
        expected = (RuntimeError, OUTPUT_SPEECH_REQUIRED_ERROR)
        with self.assertRaisesMessage(*expected):
            EchoResponse()

    def test_correct_response_body(self):
        """EchoResponse should have the correct response body"""
        expected = {
            "version": "1.0",
            "response": {
                "outputSpeech": self.output_speech,
                "card": None,
                "reprompt": None,
                "shouldEndSession": True
            },
            "sessionAttributes": {}
        }
        data = self._get_response_data(EchoResponse, output_speech=self.output_speech)
        assert data == expected

    def test_populates_session(self):
        """EchoResponse should populate the session attributes"""
        expected = {'apple': 'red', 'orange': 'orange'}
        data = self._get_response_data(EchoResponse, output_speech=self.output_speech, session=expected)
        assert data['sessionAttributes'] == expected

    def test_sets_end_session_bool(self):
        """EchoResponse should be able to set the shouldEndSession bool"""
        data = self._get_response_data(EchoResponse, output_speech=self.output_speech, should_end_session=False)
        assert not data['response']['shouldEndSession']

    def test_sets_card(self):
        """EchoResponse should be able to set the card data"""
        expected = {
            "type": SIMPLE_CARD,
            "title": "Card title",
            "content": "Some content",
        }
        response = EchoTextResponse('text', card=expected)
        data = json.loads(response.content.decode())
        assert data['response']['card'] == expected

    def test_sets_reprompt(self):
        """EchoResponse should be able to set the reprompt"""
        expected = "Did you forget to do the thing?"
        response = EchoTextResponse('text', reprompt=expected)
        data = json.loads(response.content.decode())
        assert data['response']['reprompt'] == expected


class TestEchoTextResponse(BaseEchoTestCase):
    def test_populates_text_in_response(self):
        """The Plain text response should populate the outputSpeech"""
        expected = "This is the text"
        response = EchoTextResponse(expected)
        data = json.loads(response.content.decode())

        assert data['response']['outputSpeech']['type'] == PLAIN_TEXT_OUTPUT
        assert data['response']['outputSpeech']['text'] == expected


class TestEchoSSMLResponse(BaseEchoTestCase):
    def test_populates_ssml_in_response(self):
        """The Plain text response should populate the outputSpeech"""
        expected = "<speak>This is the text</speak>"
        response = EchoSSMLResponse(expected)
        data = json.loads(response.content.decode())

        assert data['response']['outputSpeech']['type'] == SSML_OUTPUT
        assert data['response']['outputSpeech']['ssml'] == expected
