# Simple Django Twitter Authentication

**Simple Django Twitter Auth** is an explicit, simple way to add "Login with Twitter" functionality to your Django project. The goal is to keep control in your hands, and to allow customization and implementation without having to dig through pages of documentation.

## Installation

1. `pip install simple-django-twitter-auth`

2. Go to [https://apps.twitter.com](https://apps.twitter.com) and register an app if you haven't already
	- Make sure the "Allow this application to be used to Sign in with Twitter" option is enabled in your "settings" page!

3. Grab your `API key` and `API secret` from your Twitter app dashboard

4. Define the following settings in `settings.py`

	`TWITTER_APP_KEY = 'myappkey'`  
	`TWITTER_APP_SECRET = 'myappsecret'`

	*It's recommended you use [environment variables](http://andrewtorkbaker.com/using-environment-variables-with-django-settings) instead of defining confidential credentials in your settings file*

5. Define `HOST` in `settings.py`

	`HOST = 'https://3efed1b4.ngrok.com'`

	**Don't include a trailing backslash**

	**GOOD:** `https://3efed1b4.ngrok.com`  
	**BAD:**  `https://3efed1b4.ngrok.com/`

6. Add 'django_twitter_auth' to your `INSTALLED_APPS` in `settings.py`.

7. Add the following line to the top of your root `urls.py`

	`url(r'^twitter/', include('django_twitter_auth.urls', namespace='django_twitter_auth')),`

8. Run migrate to install the `TwitterProfile` model that comes with Simple Django Twitter Auth

	`python manage.py migrate`

9. That's it! You can now use the `{% url 'django_twitter_auth:login' %}` template tag to kick off the login flow.

## Login Flow

1. Simple Django Twitter Auth provides the following URL `/twitter/login/`. First, you point users here.
	- you can also utilize the `{% url 'django_twitter_auth:login' %}` template tag

2. Users are redirected to Twitter where they authorize your application, granting it access to their Twitter profile.

3. After authorizing your app, Twitter redirects users back to your site. Simple Django Twitter Auth then does one of the following:
	- Creates a new `TwitterProfile` and `User`
	- Finds an existing `TwitterProfile` and `User`
	- Finds an existing `TwitterProfile` and `User`, and updates the `TwitterProfile`'s OAuth2 tokens. *(if a Twitter user revoked access to your app, and then re-authorizes it later, Simple Django Twitter Auth simply updates the access tokens.)*

4. Simple Django Twitter Auth manually logs in the user, and redirects them back to the page they started the flow from.

## Components

### TwitterProfile

Simple Django Twitter Auth provides a `TwitterProfile` model. This model has the following attributes:

**TwitterProfile.OAUTH_TOKEN**

OAuth2 token provided by Twitter during authorization. Can be used to consume/publish additional data on behalf of Twitter User.

**TwitterProfile.OAUTH_TOKEN_SECRET**

OAuth2 token secret provided by Twitter during authorization. Can be used to consume/publish additional data on behalf of Twitter User.

**TwitterProfile.username**

User's Twitter username. '@' not included.

**TwitterProfile.user**

Whenever a new `TwitterProfile` is created, a `User` is also created and a OneToOne relationship is established with the `TwitterProfile`.

The `username` attribute of the `User` is set to the same value as `TwitterProfile.username`.

Simple Django Twitter Auth uses `django.contrib.auth.get_user_model()` to get the current `User` model.

Reverse lookup is available through `user.twitterprofile`.

## Customization

#### TWITTER_NEW_USER_URL

Define a location for new users to be redirected to. Eg:

	TWITTER_NEW_USER_URL = "/welcome/"

Users are logged in by the time they arrive here.

If this setting is defined, Simple Django Twitter Auth will append a `redir_to` URL parameter when forwarding. This will contain the URL the user started the login flow from. For example, `?redir_to=https://3efed1b4.ngrok.com/random-page/`.

You can catch this parameter to redirect the user back to where they started after you're done any custom logic defined in your `TWITTER_NEW_USER_URL` view.

#### TWITTER_AUTH_RANDOM_PASSWORD 

Default is `True`.

When Simple Django Twitter Auth creates a `User` and ties it to the `TwitterProfile`, a random base64 encoded 128-bit password using `os.urandom()` is created for the `User`. This is just a protective measure, so that the `User` isn't created with a blank password.

You can turn this off if you want, by setting `TWITTER_AUTH_RANDOM_PASSWORD` to `False`.

## Running Tests

You can manually run Simple Django Twitter Auth's tests by calling `python manage.py test django_twitter_auth` 

You'll need to install the following packages in order for the tests to work:

	pip install model-mommy
	pip install mock

## Compatability

Simple Django Twitter Auth has only been tested with Python 2.7 and Django 1.7. 

Further compatability tests will be posted shortly. If you install the app into your project using Django < 1.7 and/or Python >= 3, and it works, please update the readme! 

## Coming Soon 

- Signals to provide additional customization
- Pictures in the readme
- Better example
- More coming soon...