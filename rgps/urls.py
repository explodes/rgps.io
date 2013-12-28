from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('rgps.app.urls', namespace='app')),
                       url(r'^api/', include('rgps.api.urls', namespace='api')),
)


