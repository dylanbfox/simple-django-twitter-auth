import base64
import os

from django.db import models
from django.conf import settings

from twython import Twython

class TwitterProfile(models.Model):

	def __unicode__(self):
		return self.username

	def save(self, *args, **kwargs):
		if not self.pk:
			twitter = Twython(
				settings.TWITTER_APP_KEY,
				settings.TWITTER_APP_SECRET,
				self.OAUTH_TOKEN,
				self.OAUTH_TOKEN_SECRET
			)
			response = twitter.verify_credentials()
			self.username = response['screen_name']

			from django.contrib.auth import get_user_model
			User = get_user_model()

			# check if re-authenticating pre-existing Twitter user
			_existing_user = User.objects.filter(username=self.username)
			if _existing_user:
				user = _existing_user[0]
				profile = user.twitterprofile
				profile.OAUTH_TOKEN = self.OAUTH_TOKEN
				profile.OAUTH_TOKEN_SECRET = self.OAUTH_TOKEN_SECRET
				profile.save()
				return

			if settings.__dict__['_wrapped'].__dict__.get(
				'TWITTER_AUTH_RANDOM_PASSWORD', True
			):
				password = base64.b64encode(os.urandom(16))
			else:
				password = ""

			user = User.objects.create_user(
				username=self.username,
				password=password
			)
			self.user = user
		super(TwitterProfile, self).save(*args, **kwargs)

	OAUTH_TOKEN = models.CharField(max_length=199, blank=True, null=True)
	OAUTH_TOKEN_SECRET = models.CharField(max_length=199, blank=True, null=True)

	username = models.CharField(max_length=500, blank=True, null=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
