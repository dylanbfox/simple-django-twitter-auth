from django.conf.urls import patterns, include, url 

from django_twitter_auth import views

urlpatterns = patterns('',
	url(r'^login/$', views.login, name='login')
)