from bson import ObjectId
from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, collection='users'):
        super().__init__(collection)

    def all(self):
        return self.client.db.users.find({})

    def add_user(self, tweet):
        profile = self.get_profile(user=tweet.get('user'))
        initial_count = self.get_initial_count()
        initial_validation = self.get_initial_validation()

        return self.update_or_create(profile, {**initial_count, **initial_validation})

    def update_or_create(self, profile, initial_count):
        user = self.client.db.users.find_one(profile)

        if user is None:
            user = self.client.db.users.insert_one({**profile, **initial_count})
            print('User from insertion:', user)

            return {
                'user_id': user.inserted_id,
                'profile': profile,
            }

        self.client.db.users.update_one(profile, {'$set': initial_count})

        return {
            'user_id': ObjectId(user.get('_id')),
            'profile': profile,
        }

    def reset_counters(self):
        self.client.db.users.update_many({}, {
            '$set': {
                'retweet_count': 0,
                'favorite_count': 0,
                'tweets_count': 0
            }
        })

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
        }

    @staticmethod
    def get_initial_validation():
        return {
            'validated': None
        }

