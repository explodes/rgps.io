from django.conf import settings

def settings(request):
    return {
        'GPS_UPDATE_FRQ' : settings.GPS_UPDATE_FRQ,
        'GPS_UPDATE_COUNT' : settings.GPS_UPDATE_COUNT,
    }