from bson import ObjectId
from helpers import str2bool

from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, collection='users'):
        super().__init__(collection)

    def top_users(self):
        match = {'validated': str2bool('false')}

        users = self.client.db.users.aggregate([
            {
                '$match': match
            },
            {
                '$project': self._get_user_projection()
            },
            {
                '$sort': {'total': -1}
            },
            {
                '$limit': 5
            }
        ])

        return list(users)

    def all(self, validated='true'):
        match = {}

        if validated is not None:
            match.update({'validated': str2bool(validated)})

        users = self.client.db.users.aggregate([
            {
                '$match': match
            },
            {
                '$project': self._get_user_projection()
            },
            {
                '$sort': {'total': -1}
            }
        ])

        return list(users)

    def add_user(self, tweet):
        profile = self._get_profile(user=tweet.get('user'))
        initial_count = self._get_initial_count()
        initial_validation = self._get_initial_validation()

        return self.update_or_create(profile, {**initial_count, **initial_validation})

    def update_or_create(self, profile, initial_status):
        user = self.client.db.users.find_one(profile)

        if user is None:
            user = self.client.db.users.insert_one({**profile, **initial_status})

            return {
                'user_id': user.inserted_id,
                'profile': profile,
            }

        self.client.db.users.update_one(profile, {'$set': initial_status})
        # TODO: hay que pasar solo la inicialización, no la validación

        return {
            'user_id': ObjectId(user.get('_id')),
            'profile': profile,
        }

    def reset_counters(self):
        self.client.db.users.update_many({}, {
            '$set': self._get_initial_count()
        })

    def reset_counters_for_user(self, twitter_id):
        self.client.db.users.update_one({'twitter_id': twitter_id}, {
            '$set': self._get_initial_count()
        })

    @staticmethod
    def _get_profile(user):
        profile = {
            'twitter_id': user.get('id'),
            'twitter_name': user.get('name')
        }

        return profile

    @staticmethod
    def _get_initial_count():
        return {
            'retweet_count': 0,
            'favorite_count': 0,
            'tweets_count': 0,
        }

    @staticmethod
    def _get_initial_validation():
        return {
            'validated': False
        }

    @staticmethod
    def _get_user_projection():
        return {
            '_id': 0,
            'twitter_id': 1,
            'twitter_name': 1,
            'total': {'$sum': ['$retweet_count', '$favorite_count', '$tweets_count']},
            'retweet_count': 1,
            'favorite_count': 1,
            'tweets_count': 1
        }
