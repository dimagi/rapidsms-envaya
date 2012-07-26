import datetime

from django.http import HttpResponse, HttpResponseForbidden
from rapidsms.backends.http import RapidHttpBackend # typo on their part :-/ goes to show how well maintained this code is..
import json, time, sha, base64
import phonenumbers
from models import EnqueuedMessage

class EnvayaSMSBackend(RapidHttpBackend):
    """
    A RapidSMS Backend for EnvayaSMS

    Depends on 

    https://github.com/youngj/EnvayaSMS
    """

    def configure(self, url=None, password=None, max_delay=None, **kwargs):
        self.url = url
        self.password = password
        self.max_delay = max_delay
        super(EnvayaSMSBackend, self).configure(**kwargs)

    def handle_request(self, request):
        self.debug('Request: %s' % request.POST)
        data = request.POST

        params = ','.join('%s=%s' % (k, request.POST[k]) for k in sorted(request.POST.keys()))

        if self.password is not None:
            secure_key = sha.new(','.join((self.url, params, self.password))).digest()
            if base64.b64decode(request.META.get('HTTP_X_REQUEST_SIGNATURE', '')) != secure_key:
                return HttpResponseForbidden(json.dumps({'error': {'message': 'Bad password'}}))

        action = data.get('action', '')
        if action == 'incoming':
            message = self.message(request.POST)
            if message:
                self.route(message)
        elif action == 'outgoing':
            # send back outgoing
            phone_number = request.POST.get('phone_number', '')
            if not phone_number.startswith('+'):
                phone_number = '+%s' % phone_number
            print phone_number
            phone_number = phonenumbers.parse(phone_number)
            messages = EnqueuedMessage.messages_for(phone_number.country_code, self.max_delay)
            events = [{'event': 'send', 'messages': [{'to': data.recipient, 'message': data.message} for data in messages]}]
            messages.delete()

            return HttpResponse(json.dumps({'events': events}), content_type='application/json')
        elif action == 'send_status':
            pass
        elif action == 'device_status':
            pass
        elif action == 'forward_sent':
            pass
        elif action == 'amqp_started':
            pass
        return HttpResponse('{"events": []}', content_type='application/json')

    def message(self, data):
        if data.get('message_type') != 'call': # not sure how to handle incoming calls - ignore?
            sender = data.get('from', '')
            sms = data.get('message', '')
        return super(EnvayaSMSBackend, self).message(sender, sms)

    def send(self, message):
        m = EnqueuedMessage(recipient=message.connection.identity, message=message.text)
        m.save()
