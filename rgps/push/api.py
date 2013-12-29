import threading
import time

from django.conf import settings

from rgps.push.pygcm import GcmClient

BACK_OFF_T0 = 40
BACK_OFF_ATTEMPTS = 10


def gps_request(user):
    client = GcmClient(settings.GCM_API_KEY)
    regIds = [user.registration_id]
    data = {
        'action': 'gps',
        'frequency': settings.GPS_UPDATE_FRQ,
        'count': settings.GPS_UPDATE_COUNT
    }
    try:
        response = client.send(regIds, data)
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


def gps_request_with_backoff(user, attempts=BACK_OFF_ATTEMPTS, t0millis=BACK_OFF_T0):
    attempt = 1
    wait = t0millis * 0.001
    while attempt < BACK_OFF_ATTEMPTS:
        success = gps_request(user)
        if success:
            return True
        else:
            wait *= 2
            print 'Back off for: %s' % wait
            time.sleep(wait)
            attempt += 1
    return False


def threaded_gps_request_with_backoff(user, attempts=BACK_OFF_ATTEMPTS, t0millis=BACK_OFF_T0):
    thread = threading.Thread(target=gps_request_with_backoff,
                              args=(user,),
                              kwargs={
                                  'attempts': attempts,
                                  't0millis': t0millis
                              })
    thread.start()
    return thread