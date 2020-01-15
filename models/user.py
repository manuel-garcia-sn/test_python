from bson import ObjectId

from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
from mongo_client import MongoClient


class User:
    def __init__(self):
        self.client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE,
        )

    def drop_collection(self):
        self.client.db.users.drop()

    def add_user(self, tweet):
        profile = self.get_profile(user=tweet.get('user'))
        initial_count = self.get_initial_count()

        return self.update_or_create(profile, initial_count)

    def update_or_create(self, profile, initial_count):
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

    @staticmethod
    def get_profile(user):
        profile = {
            'twitter_id': user.get('id'),
            'twitter_name': user.get('name')
        }

        return profile

    @staticmethod
    def get_initial_count():
        return {
            'retweet_count': 0,
            'favorite_count': 0,
            'tweets_count': 0,
            'validated': None
        }

