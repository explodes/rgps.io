from django.conf import settings
from gcm import GCM

gcm = GCM(settings.GCM_API_KEY)


def send_gps_request_to_user(user):
    regIds = [user.registration_id]
    data = {'action': 'gps', 'frequency': settings.GPS_UPDATE_FRQ, 'count': settings.GPS_UPDATE_COUNT}
    try:
        gcm.json_request(registration_ids=regIds, data=data)
    except:
        ## TODO: Back off
        pass