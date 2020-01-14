from datetime import datetime

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

    def add_tweets_to_feed(self, query='sngularrocks'):
        tweets = self._get_tweets_from_api(query)

        for tweet in tweets:
            user = self._set_user(tweet=tweet)
            self._set_tweet_from_user(tweet=tweet, user=user)

    @staticmethod
    def _get_tweets_from_api(query):
        twitter_api = TwitterApi()
        tweets = twitter_api.tweets(query)

        return tweets

    def _set_user(self, tweet):
        twitter_user = tweet.get('user')

        # Insert or update user in users collection
        user = self.client.db.users.find_one({
            'twitter_id': twitter_user.get('id'),
            'twitter_name': twitter_user.get('name')
        })

        if user is None:
            user = self.client.db.users.insert_one({
                'twitter_id': twitter_user.get('id'),
                'twitter_name': twitter_user.get('name'),
                'retweet_count': 0,
                'favorite_count': 0,
                'tweets_count': 0,
                'validated': None
            })
        else:
            self.client.db.users.update_one({
                'twitter_id': twitter_user.get('id'),
                'twitter_name': twitter_user.get('name')
            }, {
                '$set': {
                    'retweet_count': 0,
                    'favorite_count': 0,
                    'tweets_count': 0,
                    'validated': None
                },
            })

        print(user)
        return user

    def _set_tweet_from_user(self, tweet, user):
        # Insert or update tweets from a given user in feed collection
        self.client.db.feed.update_one(
            {
                'twitter_id': tweet.get('id'),
                'title': tweet.get('text'),
                'link': 'https://twitter.com/{}/status/{}'.format(
                    tweet.get('user').get('screen_name'),
                    tweet.get('id')
                ),
                'user': user.get('_id')
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


t = TwitterService()
t.add_tweets_to_feed()
