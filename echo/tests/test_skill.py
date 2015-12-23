import mock

from echo.skill import (
    LAUNCH_NOT_IMPLEMENTED_ERROR,
    EchoSkill,
)
from echo.tests import BaseEchoTestCase


class TestSkill(EchoSkill):
    def the_intent(self, request, **kwargs):
        return self.respond('output speech', should_end_session=False)


class EchoSkillTestCase(BaseEchoTestCase):
    def setUp(self):
        super(EchoSkillTestCase, self).setUp()
        self.skill = TestSkill()

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

        with mock.patch.object(self.skill, 'the_intent') as mock_intent:
            self.skill.dispatch(http_request)
            assert mock_intent.call_count == expected

    def test_routes_to_intent_with_slot_kwargs(self):
        """A IntentRequest should be routed to the proper intent handler with the request and slot kwargs"""
        expected = {
            'sign': 'Virgo',
            'believes_in_horoscopes': False
        }

        slots = {
            'Sign': {
                'name': 'Sign',
                'value': 'Virgo'
            },
            'BelievesInHoroscopes': {
                'name': 'BelievesInHoroscopes',
                'value': False
            }
        }

        http_request = self._generate_intent_request(
            intent_name="TheIntent",
            slots=slots
        )

        with mock.patch.object(self.skill, 'the_intent') as mock_intent:
            self.skill.dispatch(http_request)
            mock_intent.assert_called_once_with(self.skill.request, **expected)

    def test_handles_slots_without_values(self):
        """An IntenteRequest with unassigned slot values should not cause an error"""
        expected = {
            'sign': 'Virgo',
            'believes_in_horoscopes': None
        }

        slots = {
            'Sign': {
                'name': 'Sign',
                'value': 'Virgo'
            },
            'BelievesInHoroscopes': {}
        }

        http_request = self._generate_intent_request(
            intent_name="TheIntent",
            slots=slots
        )

        with mock.patch.object(self.skill, 'the_intent') as mock_intent:
            self.skill.dispatch(http_request)
            mock_intent.assert_called_once_with(self.skill.request, **expected)

    def test_respond_generates_an_echo_request(self):
        """The respond mothed should act as a pass-through to EchoRequest"""
        expected = 'output speech'
        expected_kwargs = {'should_end_session': False, 'session': {}}

        http_request = self._generate_intent_request(intent_name="TheIntent")

        with mock.patch('echo.skill.EchoResponse') as mock_response:
            self.skill.dispatch(http_request)
            mock_response.assert_called_once_with(expected, **expected_kwargs)
