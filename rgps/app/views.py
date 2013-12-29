import threading

from django import http
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from rgps.push import api

User = get_user_model()


class IndexView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(self.request, user)
            return http.HttpResponseRedirect(reverse('app:map'))
        else:
            return self.get(request, *args, **kwargs)


class MapView(TemplateView):
    template_name = 'map.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        return super(MapView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        threading.Thread(target=api.send_gps_request_to_user, args=(user,)).start()
        return {}


