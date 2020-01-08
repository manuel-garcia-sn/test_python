import settings
import requests
from requests.auth import HTTPBasicAuth


class TwitterApi:
    def __init__(self):
        self.url = 'https://api.twitter.com/'
        self.token = ''

    def get_tweets(self):
        while self.get_response_from_twitter().status_code != 200:
            self.set_token()

        response = self.get_response_from_twitter()
        print(response.json())

        return response.json()

    def set_token(self):
        payload = {
            'grant_type': 'client_credentials'
        }
        response = requests.post(
            self.url + 'oauth2/token',
            params=payload,
            auth=HTTPBasicAuth(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        )

        self.token = response.json()['access_token']

    def get_response_from_twitter(self):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = {
            'q': '#sngularrocks',
            'lang': 'es'
        }
        response = requests.get(self.url + '1.1/search/tweets.json', params=payload, headers=headers)

        return response


t = TwitterApi()
t.get_tweets()


