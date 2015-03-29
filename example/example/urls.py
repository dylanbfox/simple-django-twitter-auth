from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('pages.urls', namespace='pages')),	
	url(r'^twitter/', include('django_twitter_auth.urls', namespace='django_twitter_auth')),
    url(r'^admin/', include(admin.site.urls)),
)
