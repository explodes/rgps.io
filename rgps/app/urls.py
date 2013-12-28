from django.conf.urls import patterns, url

from rgps.app import views

urlpatterns = patterns('rgps.app.views',
                       url('^$', views.IndexView.as_view(), name='index'),
                       url('^map/$', views.MapView.as_view(), name='map'),
                       url('^gps/$', 'gps', name='gps'),
)
