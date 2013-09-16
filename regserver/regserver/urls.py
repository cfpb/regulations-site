from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'', include('regulations.urls')),
    url(r'^eregulations/', include('regulations.urls')),
)
