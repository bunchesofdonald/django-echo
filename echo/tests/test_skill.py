import mock

from echo.skill import (
    LAUNCH_NOT_IMPLEMENTED_ERROR,
    SESSION_ENDED_NOT_IMPLEMENTED_ERROR,
    EchoSkill,
)
from echo.tests import BaseEchoTestCase


class TestEchoSkill(BaseEchoTestCase):
    def setUp(self):
        super(TestEchoSkill, self).setUp()
        self.skill = EchoSkill()

    def test_routes_to_launch(self):
        """A LaunchRequest should raise a NotImplementedError"""
        expected = (NotImplementedError, LAUNCH_NOT_IMPLEMENTED_ERROR)

        http_request = self._generate_launch_request()
        with self.assertRaisesMessage(*expected):
            self.skill.dispatch(http_request)

    def test_routes_to_session_ended(self):
        """A SessionEndedRequest should return a 200 OK"""
        expected = 200

        http_request = self._generate_session_ended_request()
        response = self.skill.dispatch(http_request)
        assert response.status_code == expected

    def test_get_intent_handler_name(self):
        """get_intent_handler_name should know how to un-camelcase a string"""
        expected = "this_is_a_camel_cased_string"
        assert self.skill.get_intent_handler_name("ThisIsACamelCasedString") == expected

    def test_routes_to_intent(self):
        """A IntentRequest should be routed to the proper intent handler"""
        expected = 1

        http_request = self._generate_intent_request(intent_name="TheIntent")

        self.skill.the_intent = None
        with mock.patch.object(self.skill, 'the_intent') as mock_intent:
            self.skill.dispatch(http_request)
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

        http_request = self._generate_intent_request(
            intent_name="TheIntent",
            slots=expected['slots'],
            session=expected['session']
        )

        self.skill.the_intent = None
        with mock.patch.object(self.skill, 'the_intent') as mock_intent:
            self.skill.dispatch(http_request)
            mock_intent.assert_called_once_with(**expected)
