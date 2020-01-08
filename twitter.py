import settings
import requests
import datetime
from requests.auth import HTTPBasicAuth
from mongo_client import MongoClient


class TwitterApi:
    def __init__(self):
        self.url = 'https://api.twitter.com/'
        self.token = ''

    def get_tweets(self):
        while self.get_response_from_twitter().status_code != 200:
            self.set_token()

        response = self.get_response_from_twitter()
        client = MongoClient()

        for tweet in response.json()['statuses']:
            data = {
                'type': 'tweet',
                'internal_id': tweet['id'],
                'title': tweet['text'],
                'user': {
                    'name': tweet['user']['name'],
                    'screen_name': tweet['user']['screen_name'],
                },
                'created_at': datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y')
            }

            if client.collection.find_one({'type': 'tweet', 'internal_id': tweet['id']}) is None:
                client.collection.insert_one(data)

        return response.json()['statuses']

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
            'q': 'sngularrocks',
            'lang': 'es',
            'count': 50
        }
        response = requests.get(self.url + '1.1/search/tweets.json', params=payload, headers=headers)

        return response


t = TwitterApi()
t.get_tweets()
