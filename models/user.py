from bson import ObjectId

from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, collection='users'):
        super().__init__(collection)

    def all(self, validated):
        match = {}
        if validated == 'true':
            match.update({'validated': True})
        elif validated == 'false':
            match.update({'validated': False})

        users = self.client.db.users.aggregate([
            {
                '$match': match
            },
            {
                '$project': {
                    '_id': 0,
                    'twitter_id': 1,
                    'twitter_name': 1,
                    'total': {'$sum': ['$retweet_count', '$favorite_count', '$tweets_count']},
                    'retweet_count': 1,
                    'favorite_count': 1,
                    'tweets_count': 1
                }
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
            print('User from insertion:', user)

            return {
                'user_id': user.inserted_id,
                'profile': profile,
            }

        self.client.db.users.update_one(profile, {'$set': initial_status})
        # hay que pasar solo la inicialización, no la validación

        return {
            'user_id': ObjectId(user.get('_id')),
            'profile': profile,
        }

    def reset_counters(self):
        self.client.db.users.update_many({}, {
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
