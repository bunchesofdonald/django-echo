# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from echo.response import (
    create_link_account_card,
    create_simple_card,
    EchoResponse,
    LINK_ACCOUNT_CARD,
    PLAIN_TEXT_OUTPUT_TYPE,
    SIMPLE_CARD,
    SSML_OUTPUT_TYPE,
)
from echo.tests import BaseEchoTestCase


class TestEchoResponse(BaseEchoTestCase):
    def setUp(self):
        super(TestEchoResponse, self).setUp()

    def test_correct_response_body(self):
        """EchoResponse should have the correct response body"""
        expected = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": PLAIN_TEXT_OUTPUT_TYPE,
                    "text": "Some plain text content"
                },
                "card": None,
                "reprompt": None,
                "shouldEndSession": True
            },
            "sessionAttributes": {}
        }
        data = self._get_response_data("Some plain text content")
        assert data == expected

    def test_correct_content_type(self):
        """EchoResponse should have the correct content type"""
        expected = ('Content-Type', 'application/json;charset=UTF-8')
        response = EchoResponse('text')
        assert response._headers['content-type'] == expected

    def test_populates_session(self):
        """EchoResponse should populate the session attributes"""
        expected = {'apple': 'red', 'orange': 'orange'}
        data = self._get_response_data("Some plain text content", session=expected)
        assert data['sessionAttributes'] == expected

    def test_sets_end_session_bool(self):
        """EchoResponse should be able to set the shouldEndSession bool"""
        data = self._get_response_data("Some plain text content", should_end_session=False)
        assert not data['response']['shouldEndSession']

    def test_sets_card(self):
        """EchoResponse should be able to set the card data"""
        expected = {
            "type": SIMPLE_CARD,
            "title": "Card title",
            "content": "Some content",
        }
        data = self._get_response_data("Some plain text content", card=expected)
        assert data['response']['card'] == expected

    def test_is_ssml_with_ssml(self):
        """is_ssml should be able to detect that a given string is SSML when given SSML"""
        ssml = """
            <speak>
                Here is a number <w role="ivona:VBD">read</w> as a cardinal number:
                <say-as interpret-as="cardinal">12345</say-as>.
                Here is a word spelled out: <say-as interpret-as="spell-out">hello</say-as>.
            </speak>
        """
        response = EchoResponse("Some plain text content")
        assert response.is_ssml(ssml)

    def test_is_ssml_with_plain_text(self):
        """is_ssml should be able to detect that a given string is not SSML when given plain text"""
        text = "This is just some text"
        response = EchoResponse("Some plain text content")
        assert not response.is_ssml(text)

    def test_text_output_speech(self):
        """EchoResponse should respond with a plain text output speech when given plain text"""
        expected = {
            "type": PLAIN_TEXT_OUTPUT_TYPE,
            "text": "Just some plain text"
        }
        data = self._get_response_data(expected['text'])
        assert data['response']['outputSpeech'] == expected

    def test_ssml_output_speech(self):
        """EchoResponse should respond with an SSML output speech when given SSML"""
        expected = {
            "type": SSML_OUTPUT_TYPE,
            "ssml": "<speak>This is the text</speak>"
        }
        data = self._get_response_data(expected['ssml'])
        assert data['response']['outputSpeech'] == expected

    def test_text_reprompt(self):
        """EchoResponse should respond with a plain text reprompt when given plain text"""
        expected = {
            "type": PLAIN_TEXT_OUTPUT_TYPE,
            "text": "Did you forget to do the thing?"
        }
        data = self._get_response_data("Content", reprompt=expected['text'])
        assert data['response']['reprompt'] == expected

    def test_populates_ssml_output_speech(self):
        """EchoResponse should response with an SSML reprompt when given SSML"""
        expected = {
            "type": SSML_OUTPUT_TYPE,
            "ssml": "<speak>Did you forget to do the thing?</speak>"
        }
        data = self._get_response_data("Content", reprompt=expected['ssml'])
        assert data['response']['reprompt'] == expected

    def test_create_simple_card(self):
        """The create_simple_card helper should be able to return a valid simple card dictionary"""
        expected = {
            "type": SIMPLE_CARD,
            "title": "Card title",
            "content": "Some content",
        }

        assert create_simple_card('Card title', 'Some content') == expected

    def test_create_card_link_account_card(self):
        """The create_link_account_card helper should be able to return a valid link account card dictionary"""
        expected = {"type": LINK_ACCOUNT_CARD, }
        assert create_link_account_card() == expected

    def _get_response_data(self, *args, **kwargs):
        response = EchoResponse(*args, **kwargs)
        return json.loads(response.content.decode())
