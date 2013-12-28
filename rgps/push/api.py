import time

import requests
from django.conf import settings


GCM_ENDPOINT = "https://android.googleapis.com/gcm/send"


def send_gps_request_to_user(user):
    headers = {
        'Authentication': 'key=%s' % settings.GCM_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'registration_ids': [user.registration_id],
        'data': {
            'action': 'gps',
            'frequency': settings.GPS_UPDATE_FRQ,
            'count': settings.GPS_UPDATE_COUNT
        }
    }

    attempt = 1

    while attempt < 10:
        try:
            response = requests.post(GCM_ENDPOINT, data=data, headers=headers)
            if response.status_code != 200:
                raise Exception('Back off')
        except:
            if attempt == 10:
                return None
            time.sleep(attempt ** 2 * 12)
            attempt += 1
        else:
            return
