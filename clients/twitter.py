import sys
sys.path.append('../')
import settings
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from mongo_client import MongoClient


class TwitterApi:
    def __init__(self):
        self.url = 'https://api.twitter.com/'
        self.token = ''

    def tweets(self):
        response = self._get_response()

        if response.status_code != 200:
            self.set_token()
            response = self._get_response()

        return response.json()['statuses']

    def set_token(self):
        payload = {
            'grant_type': 'client_credentials'
        }
        response = requests.post(
            '{}oauth2/token'.format(self.url),
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
