import json
import urllib
import urllib2

GOOGLE_SEND_URL = 'https://android.googleapis.com/gcm/send'


class BaseGcmClient(object):
    def __init__(self, api_key, client=None):
        self.api_key = api_key

        # Client setup
        self._client = client(self._content_handler)

    def send(self, registration_ids, data=None, delay_while_idle=False, time_to_live=None, collapse_key=None):
        send_data = {}

        # Set registration ids
        if not isinstance(registration_ids, (list, tuple)):
            registration_ids = [registration_ids]

        send_data['delay_while_idle'] = bool(delay_while_idle)

        # time_to_live and collapse_key need to be specified both or none.
        if (time_to_live is not None) ^ (collapse_key is not None):
            raise ValueError("'time_to_live' and 'collapse_key' need to be specified both or none")
            send_data['time_to_live'] = int(time_to_live)
            send_data['collapse_key'] = collapse_key

        # the data is optional
        if data is not None:
            send_data['data'] = data

        # send
        return self._client.send(self.api_key, registration_ids, send_data)


class JsonHandler(object):
    content_type = 'application/json'

    def dump(self, registration_ids, send_data):
        send_data['registration_ids'] = registration_ids
        return json.dumps(send_data)

    def load(self, data):
        return json.loads(data)


class PlainTextHandler(object):
    content_type = 'application/x-www-form-urlencoded;charset=UTF-8'

    def dump(self, registration_ids, send_data):
        # Check registration_ids
        if len(registration_ids) != 1:
            raise ValueError("Only one registration_id allowed for plaintext")
        send_data['registration_id'] = registration_ids[0]

        # Flat data
        if 'data' in send_data:
            data = send_data.pop('data')
            d = dict([('data_%s' % k, v) for k, v in data.iteritems()])
            send_data.update(d)
        serialized_data = urllib.urlencode(send_data)
        return serialized_data

    def load(self, data):
        return data


CONTENT_HANDLERS = {
    'json': JsonHandler,
    'plaintext': PlainTextHandler,
}


class HTTPClient(object):
    url = GOOGLE_SEND_URL

    def __init__(self, handler):
        self._handler = handler()


class Urllib2Client(HTTPClient):
    immediate_return = False

    def _gotResponse(self, result):
        pass

    def send(self, api_key, registration_ids, send_data):
        headers = {
            'Content-Type': self._handler.content_type,
            'Authorization': 'key=%s' % api_key
        }
        x = self._handler.dump(registration_ids, send_data)
        print x
        request = urllib2.Request(
            self.url,
            self._handler.dump(registration_ids, send_data),
            headers
        )
        response = urllib2.urlopen(request).read()
        return self._handler.load(response)


class GcmClient(BaseGcmClient):
    def __init__(self, api_key, mode='json', client=Urllib2Client):
        try:
            self._content_handler = CONTENT_HANDLERS[mode]
        except KeyError:
            modes = ' or '.join(CONTENT_HANDLERS.keys())
            raise ValueError('"mode" must be %s' % modes)
        super(GcmClient, self).__init__(api_key, client=client)