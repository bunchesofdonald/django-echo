import logging
import re

from django import http
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .request import EchoRequest


log = logging.getLogger(__name__)

LAUNCH_NOT_IMPLEMENTED_ERROR = "'launch' is not implemented. Implement this handler in a base class."
SESSION_ENDED_NOT_IMPLEMENTED_ERROR = "'session ended' is not implemented. Implement this handler in a base class."


class EchoSkill(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, http_request):
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
        return getattr(self, handler_name)(
            slots=requested_intent.get('slots', {}),
            session=self.request.session
        )

    def get_intent_handler_name(self, intent_name):
        return re.sub('(?!^)([A-Z])', r'_\1', intent_name).lower()
