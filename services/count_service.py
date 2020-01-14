from bson import ObjectId
from mongo_client import MongoClient
from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE


class CountService:
    def __init__(self):
        self.client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE
        )

    def calculate_count(self):
        self._reset_counters()
        self._process_feed()

    def _reset_counters(self):
        self.client.db.users.update_many(
            {},
            {
                '$set': {
                    'retweet_count': 0,
                    'favorite_count': 0,
                    'tweets_count': 0
                }
            })

    def _process_feed(self):
        for user in self.client.db.users.find({}):
            user_id = user.get('_id')
            tweets = self.client.db.feed.find({'user': ObjectId(user_id)})
            self._process_user_tweets(user_id=user_id, tweets=tweets)

    def _process_user_tweets(self, user_id, tweets):
        for tweet in tweets:
            self._update_user_count(
                user_id=user_id,
                tweet=tweet,
            )

    def _update_user_count(self, user_id, tweet):
        self.client.db.users.update_one(
            {'_id': user_id},
            {
                '$inc': {
                    'retweet_count': tweet.get('retweet_count'),
                    'favorite_count': tweet.get('favorite_count'),
                    'tweets_count': 1
                }
            }
        )


c = CountService()
c.calculate_count()
