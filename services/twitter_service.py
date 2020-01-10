import sys
sys.path.append('../')

import settings
from datetime import datetime
from clients.twitter import TwitterApi
from mongo_client import MongoClient


class TwitterService:
    @staticmethod
    def add_tweets_to_feed():
        client = MongoClient(
            host=settings.MONGODB_HOST,
            port=settings.MONGODB_PORT,
            db=settings.MONGODB_DATABASE,
            collection=settings.MONGODB_COLLECTION
        )

        twitter_api = TwitterApi()
        tweets = twitter_api.tweets()

        for tweet in tweets:
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


t = TwitterService()
t.add_tweets_to_feed()

