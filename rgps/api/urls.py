from django.conf.urls import patterns, url

urlpatterns = patterns('rgps.api.views',
                       url('^register/$', 'register', name='register'),
                       url('^login/$', 'login', name='login'),
                       url('^signup/$', 'signup', name='signup'),
                       url('^user/$', 'user', name='user'),
                       url('^coords/$', 'coords', name='coords'),
)