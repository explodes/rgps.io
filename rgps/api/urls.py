from django.conf.urls import patterns, include, url

urlpatterns = patterns('rgps.api.views',
                       url('register/', 'register', name='register'),
                       url('login/', 'login', name='login'),
                       url('signup/', 'signup', name='signup'),
                       url('user/', 'user', name='user'),
)