from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from rgps.c2dm import api

User = get_user_model()


class IndexView(TemplateView):
    template_name = 'index.html'


class MapView(TemplateView):
    template_name = 'map.html'


def gps(request):
    #user = request.user
    user = User.objects.get(username='explodes')
    api.send_gps_request_to_user(user)
    return http.HttpResponseRedirect(reverse('app:map'))



