import sys
import settings
import requests
from requests.auth import HTTPBasicAuth

sys.path.append('../')


class TwitterApi:
    def __init__(self):
        self.url = 'https://api.twitter.com/'
        self.token = ''

    def tweets(self):
        response = self._get_response()

        if response.status_code != 200:
            self.set_token()
            response = self._get_response()

        return response.json().get('statuses', {})

    def set_token(self):
        payload = {
            'grant_type': 'client_credentials'
        }
        response = requests.post(
            '{}{}'.format(self.url, 'oauth2/token'),
            params=payload,
            auth=HTTPBasicAuth(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        )

        self.token = response.json()['access_token']

    def _get_response(self):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        payload = {
            'q': 'sngularrocks',
            'lang': 'es',
            'count': 50
        }
        response = requests.get('{}1.1/search/tweets.json'.format(self.url), params=payload, headers=headers)

        return response


t = TwitterApi()
t.tweets()
