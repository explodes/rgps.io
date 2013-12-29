import threading
import time

import requests
from django.conf import settings


GCM_ENDPOINT = "https://android.googleapis.com/gcm/send"

BACK_OFF_T0 = 10
BACK_OFF_ATTEMPTS = 3


def gps_request(user):
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
    try:
        response = requests.post(GCM_ENDPOINT, data=data, headers=headers)
    except Exception as error:
        print 'Error sending GPS request to %s: %s' % (user, error)
        return False
    else:
        status_code = response.status_code
        if status_code != 200:
            print 'Bad status code sending GPS request to %s: %s' % (user, status_code)
            return False
        else:
            return True


def gps_request_with_backoff(user, attempts=BACK_OFF_ATTEMPTS, t0=BACK_OFF_T0):
    attempt = 1
    while attempt < BACK_OFF_ATTEMPTS:
        success = gps_request(user)
        if success:
            return True
        else:
            wait = attempt ** 2 * BACK_OFF_T0
            print 'Back off for: %s' % wait
            time.sleep(wait)
            attempt += 1
    return False


def threaded_gps_request_with_backoff(user, attempts=BACK_OFF_ATTEMPTS, t0=BACK_OFF_T0):
    thread = threading.Thread(target=gps_request_with_backoff, args=(user,), kwargs={'attempts': attempts, 't0': t0})
    thread.start()
    return thread