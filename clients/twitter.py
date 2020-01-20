from config.settings import TWITTER_KEY, TWITTER_SECRET
import requests
from requests.auth import HTTPBasicAuth


class TwitterApi:
    def __init__(self):
        self.url = 'https://api.twitter.com/'
        self.token = ''

    def tweets(self, query='sngularrocks'):
        response = self._get_response(query)

        if response.status_code != 200:
            self.set_token()
            response = self._get_response(query)

        return response.json().get('statuses', {})

    def set_token(self):
        payload = {
            'grant_type': 'client_credentials'
        }
        response = requests.post(
            '{}{}'.format(self.url, 'oauth2/token'),
            params=payload,
            auth=HTTPBasicAuth(TWITTER_KEY, TWITTER_SECRET)
        )

        self.token = response.json().get('access_token')

    def _get_response(self, query):
        print(query)
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        payload = {
            'q': query,
            'lang': 'es',
            'count': 100
        }
        response = requests.get('{}{}'.format(self.url, '1.1/search/tweets.json'), params=payload, headers=headers)

        return response


if __name__ == '__main__':
    t = TwitterApi()
    t.tweets()
