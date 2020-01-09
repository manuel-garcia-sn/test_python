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

        client = MongoClient(
            host=settings.MONGODB_HOST,
            port=settings.MONGODB_PORT,
            db=settings.MONGODB_DATABASE,
            collection=settings.MONGODB_COLLECTION
        )

        for tweet in response.json()['statuses']:
            find_urls = (tweet['entities']['urls'])

            urls = {}
            if find_urls:
                urls = {
                    'short_url': (find_urls[0])['url'],
                    'expanded_url': (find_urls[0])['expanded_url'],
                }

            data = {
                'type': 'tweet',
                'internal_id': tweet['id'],
                'title': tweet['text'],
                'link': 'https://twitter.com/{}/status/{}'.format(tweet['user']['screen_name'], tweet['id']),
                'urls': urls,
                'user': {
                    'name': tweet['user']['name'],
                    'screen_name': tweet['user']['screen_name'],
                    'profile_image_url': tweet['user']['profile_image_url_https']
                },
                'created_at': datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y')
            }

            if client.collection.find_one({'type': 'tweet', 'internal_id': tweet['id']}) is None:
                client.collection.insert_one(data)

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
