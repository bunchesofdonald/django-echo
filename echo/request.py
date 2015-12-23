import json
import logging


log = logging.getLogger(__name__)


class EchoRequest(object):
    LAUNCH_REQUEST = 'LaunchRequest'
    INTENT_REQUEST = 'IntentRequest'
    SESSION_ENDED_REQUEST = 'SessionEndedRequest'

    def __init__(self, http_request):
        self.data = json.loads(http_request.body)
        log.debug(self.data)

    @property
    def type(self):
        return self.data['request']['type']

    @property
    def intent(self):
        return self.data['request']['intent']

    @property
    def session(self):
        attributes = self.data['session'].get('attributes')
        if attributes is None:
            attributes = {}

        return attributes
