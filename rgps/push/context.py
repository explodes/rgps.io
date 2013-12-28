from django.conf import settings as s


def settings(request):
    return {
        'GPS_UPDATE_FRQ': s.GPS_UPDATE_FRQ,
        'GPS_UPDATE_COUNT': s.GPS_UPDATE_COUNT,
    }