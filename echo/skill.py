import logging
import re

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .request import EchoRequest


log = logging.getLogger(__name__)


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
        pass

    def intent(self):
        requested_intent = self.request.intent
        handler_name = self._get_intent_handler_name(requested_intent['name'])
        return getattr(self, handler_name)(requested_intent.get('slots', {}))

    def _get_intent_handler_name(self, intent_name):
        return re.sub('(?!^)([A-Z])', r'_\1', intent_name).lower()

    def session_ended(self):
        pass
