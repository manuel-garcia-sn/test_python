from datetime import datetime

import pymongo

from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
from mongo_client import MongoClient


class Post:
    def __init__(self):
        self.client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE,
        )

    def all(self, q, post_type=None):
        query = {'$text': {'$search': q}}
        if post_type:
            query.update({'type': post_type})

        print(query)

        posts = self.client.db.feed.find(query, {'_id': False}).sort([('created_at', pymongo.DESCENDING)])

        return list(posts)

    def add_tweet_from_user(self, tweet, user_id):
        self.client.db.feed.update_one(
            {
                'twitter_id': tweet.get('id'),
                'title': tweet.get('text'),
                'link': 'https://twitter.com/{}/status/{}'.format(
                    tweet.get('user').get('screen_name'),
                    tweet.get('id')
                ),
                'user': user_id
            },
            {
                '$setOnInsert': {
                    'created_at': datetime.strptime(tweet.get('created_at'), '%a %b %d %X %z %Y'),
                    'validated': None,
                },
                '$set': {
                    'retweet_count': tweet.get('retweet_count'),
                    'favorite_count': tweet.get('favorite_count')
                }
            },
            upsert=True
        )

    def drop_collection(self):
        self.client.db.feed.drop()
