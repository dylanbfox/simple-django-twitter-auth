from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth import login as django_login

from twython import Twython

from django_twitter_auth.models import TwitterProfile

def login(request):
	if request.GET.get('denied'):
		return redirect(request.GET.get('redir_to', '') or '/')

	if request.GET.get('oauth_verifier'):
		temp_token = request.session['oauth_token']
		twitter_token = request.GET.get('oauth_token')
		if temp_token != twitter_token:
			return HttpResponseForbidden()

		oauth_verifier = request.GET['oauth_verifier']
		twitter = Twython(
			settings.TWITTER_APP_KEY,
			settings.TWITTER_APP_SECRET,
			request.session['oauth_token'],
			request.session['oauth_token_secret']
		)
		final_auth = twitter.get_authorized_tokens(oauth_verifier)

		profile, new = TwitterProfile.objects.get_or_create(
			OAUTH_TOKEN=final_auth['oauth_token'], # final token
			OAUTH_TOKEN_SECRET=final_auth['oauth_token_secret'], # final token
		)

		# if we updated the tokens, must refresh the instance
		try:
			profile.user
		except:
			profile = TwitterProfile.objects.get(OAUTH_TOKEN=final_auth['oauth_token'])

		profile.user.backend = 'django.contrib.auth.backends.ModelBackend'
		django_login(request, profile.user)		

		if new and settings.__dict__['_wrapped'].__dict__.get(
			'TWITTER_NEW_USER_URL', False
		): 
			return redirect(
				settings.TWITTER_NEW_USER_URL + 
				"?redir_to=" + request.GET.get('redir_to', '')
			)
		else:
			return redirect(request.GET.get('redir_to', '') or '/')

	twitter = Twython(
		settings.TWITTER_APP_KEY,
		settings.TWITTER_APP_SECRET,
	)

	callback_url = (
		settings.HOST + 
		reverse('django_twitter_auth:login') + 
		"?redir_to=" + request.META.get('HTTP_REFERER', '')
	)
	auth = twitter.get_authentication_tokens(
		callback_url=callback_url
	)
	request.session['oauth_token'] = auth['oauth_token']
	request.session['oauth_token_secret'] = auth['oauth_token_secret']
	return redirect(auth['auth_url'])