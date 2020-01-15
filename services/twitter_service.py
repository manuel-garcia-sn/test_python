from datetime import datetime

from bson import ObjectId

from clients.twitter import TwitterApi
from mongo_client import MongoClient
from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE


class TwitterService:
    def __init__(self):
        self.client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE
        )
        
        self._drop_collections()

    def add_tweets_to_feed(self, query='sngularrocks'):
        tweets = self._get_tweets_from_api(query)

        for tweet in tweets:
            user_id = self._set_user(tweet=tweet)
            self._set_tweet_from_user(tweet=tweet, user_id=user_id)

    @staticmethod
    def _get_tweets_from_api(query):
        twitter_api = TwitterApi()
        tweets = twitter_api.tweets(query)

        return tweets

    def _set_user(self, tweet):
        profile = self._get_profile(tweet.get('user'))
        initial_count = self._get_initial_count()

        user = self.client.db.users.find_one(profile)

        if user is None:
            user = self.client.db.users.insert_one({**profile, **initial_count})
            print('User from insertion:', user)
            user_id = user.inserted_id
        else:
            self.client.db.users.update_one(profile, {'$set': initial_count})

            user_id = ObjectId(user.get('_id'))
            print('User from update:', user_id)

        return {
            'user_id': user_id,
            'profile': profile,
        }

    def _set_tweet_from_user(self, tweet, user_id):
        # Insert or update tweets from a given user in feed collection
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

    def _drop_collections(self):
        self.client.db.feed.drop()
        self.client.db.users.drop()

    @staticmethod
    def _get_profile(twitter_user):
        profile = {
            'twitter_id': twitter_user.get('id'),
            'twitter_name': twitter_user.get('name')
        }

        return profile

    @staticmethod
    def _get_initial_count():
        return {
            'retweet_count': 0,
            'favorite_count': 0,
            'tweets_count': 0,
            'validated': None
        }


t = TwitterService()
t.add_tweets_to_feed()
