from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from mock import patch
from model_mommy import mommy

from django_twitter_auth.models import TwitterProfile

class LoginViewTest(TestCase):
	"""
	Tests for setting up Twitter authentication and
	redirecting user to Twitter to authorize app.
	"""

	def setUp(self):
		# setup the patch
		patcher = patch('django_twitter_auth.views.Twython') 
		self.mock_Twython = patcher.start()
		self.addCleanup(patcher.stop)

		# mock out all functionality required for view
		self.mock_auth = {
			'auth_url': 'http://faketwitterurl.com/auth/', # supplied by Twitter
			'oauth_token': 'tempoauthtoken', # supplied by Twitter
			'oauth_token_secret': 'tempoauthtokensecret', # supplied by Twitter
		}
		self.mock_Twython_instance = self.mock_Twython.return_value
		self.mock_Twython_instance.get_authentication_tokens.return_value = self.mock_auth

	@patch('django_twitter_auth.views.redirect')
	def test_view_redirects_to_auth_url(self, mock_redirect):
		pass # can't mock out redirect for some reason"

	def test_Twython_instance_initialized_with_app_tokens(self):
		response = self.client.get(
			reverse('django_twitter_auth:login')
		)
		self.mock_Twython.assert_called_once_with(
			settings.TWITTER_APP_KEY,
			settings.TWITTER_APP_SECRET,
		)

	def test_callback_url_set_to_login_view(self):
		callback_url = (
			settings.HOST +
			reverse('django_twitter_auth:login') +
			"?redir_to="
		)
		response = self.client.get(
			reverse('django_twitter_auth:login')
		)
		self.mock_Twython_instance.get_authentication_tokens.assert_called_once_with(
			callback_url=callback_url
		)

	def test_temporary_OAuth2_tokens_stored_in_session(self):
		response = self.client.get(
			reverse('django_twitter_auth:login')
		)
		self.assertEqual(
			self.client.session['oauth_token'],
			self.mock_auth['oauth_token']
		)
		self.assertEqual(
			self.client.session['oauth_token_secret'],
			self.mock_auth['oauth_token_secret']
		)

	def test_redir_param_added_to_callback_url_when_available(self):
		pass

class LoginViewCallbackTest(TestCase):
	"""
	Tests for handling the callback received
	from Twitter after user has authorized app.
	"""

	def set_temp_OAuth2_session_cookies(self):
		# setup the patch
		patcher = patch('django_twitter_auth.views.Twython') 
		self.mock_Twython = patcher.start()

		# mock out all functionality required for view
		# so session cookies can be set
		self.mock_auth = {
			'auth_url': 'http://faketwitterurl.com/auth/', # supplied by Twitter
			'oauth_token': 'tempoauthtoken', # supplied by Twitter
			'oauth_token_secret': 'tempoauthtokensecret', # supplied by Twitter
		}
		self.mock_Twython_instance = self.mock_Twython.return_value
		self.mock_Twython_instance.get_authentication_tokens.return_value = self.mock_auth

		# explicitly set session cookies by passing client thru view
		self.client.get(reverse('django_twitter_auth:login'))

		# stop the patch
		patcher.stop()

	def setUp(self):
		# explicitly set session cookies that should be set
		# before user comes back from Twitter authorization page
		self.set_temp_OAuth2_session_cookies()

		### setup the Twython patch ###
		patcher = patch('django_twitter_auth.views.Twython') 
		self.mock_Twython = patcher.start()
		self.addCleanup(patcher.stop)

		# mock out all functionality required for view
		self.mock_final_auth = {
			'oauth_token': 'finaloauthtoken', # supplied by Twitter
			'oauth_token_secret': 'finaloauthtokensecret', # supplied by Twitter
		}
		self.mock_Twython_instance = self.mock_Twython.return_value
		self.mock_Twython_instance.get_authorized_tokens.return_value = self.mock_final_auth

		### setup the get_or_create patch ###
		patcher2 = patch('django_twitter_auth.views.TwitterProfile.objects.get_or_create')
		self.mock_get_or_create = patcher2.start()
		self.addCleanup(patcher2.stop)

		# mock out all functionality required for view
		profile = mommy.make(TwitterProfile, pk=1) # manually set PK to avoid Twython call
		self.mock_get_or_create.return_value = (profile, False)

	def test_view_raises_403_if_oauth_tokens_dont_match(self):
		# Twitter will include the temp
		# oauth_token in the callback too
		response = self.client.get(
			reverse('django_twitter_auth:login') +
			"?oauth_verifier=twitteroauthverifiertoken" +
			"&oauth_token=invalidtempoauthtoken"
		)

		self.assertEqual(response.status_code, 403)	

	def test_Twython_instance_initialized_with_temp_user_OAuth2_tokens(self):
		response = self.client.get(
			reverse('django_twitter_auth:login') +
			"?oauth_verifier=twitteroauthverifiertoken" +
			"&oauth_token=" + self.client.session['oauth_token']			
		)
		self.mock_Twython.assert_called_once_with(
			settings.TWITTER_APP_KEY,
			settings.TWITTER_APP_SECRET,
			self.client.session['oauth_token'],
			self.client.session['oauth_token_secret']
		)

	def test_get_authorized_tokens_called_with_oauth_verifier_param(self):
		"""
		Exchanges temp oauth tokens for permanent ones.
		"""
		response = self.client.get(
			reverse('django_twitter_auth:login') +
			"?oauth_verifier=twitteroauthverifiertoken" +
			"&oauth_token=" + self.client.session['oauth_token']
		)
		self.mock_Twython_instance.get_authorized_tokens.assert_called_once_with(
			"twitteroauthverifiertoken"
		)

	def test_view_redirects_to_denied_view_if_denied_param_found(self):
		"""
		Twitter adds a denied param to URL if User denies
		permission at their authorization form.
		"""
		response = self.client.get(
			reverse('django_twitter_auth:login') + 
			"?denied=True"
		)
		self.assertRedirects(response, '/')

	def test_view_redirects_to_new_user_view_if_new_user_and_if_setting_defined(self):
		settings.TWITTER_NEW_USER_URL = "/new-user-url/"
		# override default mock functionality
		profile = mommy.make(TwitterProfile, pk=1) # manually set PK to avoid Twython call
		self.mock_get_or_create.return_value = (profile, True)

		response = self.client.get(
			reverse('django_twitter_auth:login') +
			"?oauth_verifier=twitteroauthverifiertoken" +
			"&oauth_token=" + self.client.session['oauth_token']
		)
		# redir_to param should be maintained thru this redirect!
		self.assertEqual(response.url[-24:], "/new-user-url/?redir_to=")

	def test_view_redirects_to_redir_param_if_no_new_user_setting_defined(self):
		response = self.client.get(
			reverse('django_twitter_auth:login') +
			"?oauth_verifier=twitteroauthverifiertoken" +
			"&oauth_token=" + self.client.session['oauth_token'] +
			"&redir_to=" + "/redirection-url/"
		)
		self.assertEqual(response.url[-17:], "/redirection-url/")

	


