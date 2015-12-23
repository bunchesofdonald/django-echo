import logging
import re

from django import http
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .request import EchoRequest
from .response import EchoResponse, create_simple_card, create_link_account_card


log = logging.getLogger(__name__)

LAUNCH_NOT_IMPLEMENTED_ERROR = "'launch' is not implemented. Implement this handler in a subclass."


class EchoSkill(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, http_request):
        self.http_request = http_request
        self.request = EchoRequest(http_request)

        handlers = {
            EchoRequest.LAUNCH_REQUEST: self.launch,
            EchoRequest.INTENT_REQUEST: self.intent,
            EchoRequest.SESSION_ENDED_REQUEST: self.session_ended,
        }

        return handlers[self.request.type]()

    def launch(self):
        raise NotImplementedError(LAUNCH_NOT_IMPLEMENTED_ERROR)

    def session_ended(self):
        return http.HttpResponse()

    def intent(self):
        requested_intent = self.request.intent
        handler_name = self.get_intent_handler_name(requested_intent['name'])

        handler_kwargs = {}
        for name, slot in requested_intent.get('slots', {}).items():
            name = self.transform_slot_name(name)
            handler_kwargs[name] = slot.get('value', None)

        return getattr(self, handler_name)(self.request, **handler_kwargs)

    def respond(self, output_speech, **kwargs):
        return EchoResponse(output_speech, session=self.request.session, **kwargs)

    def create_simple_card(self, title, content):
        return create_simple_card(title, content)

    def create_link_account_card(self, title, content):
        return create_link_account_card(title, content)

    def get_intent_handler_name(self, intent_name):
        return re.sub('(?!^)([A-Z])', r'_\1', intent_name).lower()

    def transform_slot_name(self, slot_name):
        return self.get_intent_handler_name(slot_name)
