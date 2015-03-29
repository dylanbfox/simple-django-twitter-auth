### Notes

- `settings.AUTH_USER_MODEL` is used to create OneToOne relationship with `TwitterProfile`
	- User.username == TwitterProfile.username
	- see below for password info 

- required settings:
	- `TWITTER_APP_KEY = os.environ['TWITTER_APP_KEY']`
	- `TWITTER_APP_SECRET = os.environ['TWITTER_APP_SECRET']`
	- `HOST = "http://127.0.0.1:8000"`
		- # HOST is needed for formatting the callback url sent to Twitter
- Twitter username is set to User username

- Users aren't re-created if they revoke access tokens and log back in. Their `TwitterProfile` is found via username attribute lookup, and their access tokens are simply updated to the new access tokens. 
	- happens implicitly in the `TwitterProfile.save()` method

- if allowing users to register/login using email, use:
	- `TWITTER_AUTH_RANDOM_PASSWORD` to True
		- this creates a random password for the `User` that's created and tied to
		the `TwitterProfile` so that people can't login with a username (Twitter username) and blank password.
			- base64 encoded 128 bit password using `os.urandom`
	- this is strictly precautionary, so malicious people can't try to login to the site using a twitter username and a blank password
	- **set to True by default! must set to False if you don't want this behavior** 

- `TWITTER_NEW_USER_URL`, optional
	- redirect new users to this URL, for eg, to capture an email address
	- `redir_to` URL param passed along so you can redirect user back to
	where they started if you want
	- users are logged in by the time they arrive here

- can access profile in requests like so:
	- `user.twitterprofile`
	- `user.twitterprofile.OAUTH_TOKEN`
	- `user.twitterprofile.OAUTH_TOKEN_SECRET`

- if user denies access at Twitter, they'll be redirect to page they came from (if available) OR home page

- can test app by manually running `python manage.py test django_twitter_auth`

### Installation

1. Go to https://apps.twitter.com
2. To use the “Sign in with Twitter” flow, please go to your application settings and ensure that the “Allow this application to be used to Sign in with Twitter?” option is enabled.
3. Grab your API key and API secret
4. Define the following settings:

	TWITTER_APP_KEY = 'API Key'
	TWITTER_APP_SETTINGS = 'API Secret'

*It's recommended you use environment variables instead of defining confidential credentials in here"*

	TWITTER_APP_KEY = os.environ['TWITTER_APP_KEY']
	TWITTER_APP_SECRET = os.environ['TWITTER_APP_SECRET']

5. Define HOST settings
	
	HOST = 'https://3efed1b4.ngrok.com'

**Don't include a backslash**

**GOOD:** https://3efed1b4.ngrok.com
**BAD:**  https://3efed1b4.ngrok.com/

6. Add the following line to your root urls.py

	url(r'^twitter/', include('django_twitter_auth.urls', namespace='django_twitter_auth')), 

7. Run migrate
	
	- need to install `TwitterProfile` model

7. That's it!

### Optional settings

	TWITTER_NEW_USER_URL = "/welcome/"