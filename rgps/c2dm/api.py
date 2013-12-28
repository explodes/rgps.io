

C2DM_URL = 'https://android.apis.google.com/c2dm/send'

def send_gps_request_to_user(user):
    post_params = {
        'registration_id' : user.registration_id,
        'collapse_key': 'GPS',
        'auth': user.google_oauth2,

    }