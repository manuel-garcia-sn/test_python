from config.settings import TWITTER_KEY, TWITTER_SECRET
import requests
from requests.auth import HTTPBasicAuth


class TwitterApi:
    def __init__(self):
        self.url = 'https://api.twitter.com/'
        self.token = ''

    def tweets(self, query='sngularrocks'):
        has_more_results = True
        tweets = []

        while has_more_results:
            response = self._get_response(query, has_more_results)

            if response.status_code != 200:
                self.set_token()
                response = self._get_response(query)

            has_more_results = response.json().get('search_metadata').get('next_results', False)
            query = {}
            tweets.extend(response.json().get('statuses', {}))

        return tweets

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

    def _get_response(self, query, next_results=''):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        payload = {
            'q': query,
            'count': 100,
            'tweet_mode': 'extended'
        }
        response = requests.get('{}{}{}'.format(self.url, '1.1/search/tweets.json', next_results),
                                params=payload,
                                headers=headers
                                )

        return response


if __name__ == '__main__':
    t = TwitterApi()
    t.tweets()
