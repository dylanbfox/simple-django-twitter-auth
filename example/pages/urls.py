from django.conf.urls import patterns, include, url 

from pages import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^welcome/$', views.welcome, name='welcome'),
	url(r'^random-page/$', views.random, name='random'),
)
