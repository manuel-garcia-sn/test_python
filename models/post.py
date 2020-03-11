from datetime import datetime
import pymongo
from bson import ObjectId

from models.base_model import BaseModel
from models.user import User


class Post(BaseModel):
    def __init__(self, collection='feed', elements=2):
        super().__init__(collection)
        self.paginate_elements = elements

    def all(self, q, page=1, post_type=None):
        query = {'$text': {'$search': q}}
        if post_type:
            query.update({'type': post_type})

        skip = self.calculate_skip_results(self.paginate_elements, page)

        posts = (self.client.db.feed.find(query, {'_id': False})
                 .skip(skip)
                 .limit(self.paginate_elements)
                 .sort([('created_at', pymongo.DESCENDING)])
                 )

        return list(posts)

    @staticmethod
    def calculate_skip_results(elements, page):
        return int((page - 1) * elements) if (page > 0) else int(0)

    def find_by_user_id(self, user_id):
        return self.client.db.feed.find({'user': ObjectId(user_id)})

    def find_by_user_twitter_id(self, user_tweeter_id):
        return self.client.db.feed.find(
            {'user.profile.twitter_id': user_tweeter_id, 'validated': True}
        )

    def add_tweet_from_user(self, tweet, user_id):
        media_url = ''
        if tweet.get('entities').get('media') is not None:
            media_url = tweet.get('entities').get('media')[0].get('media_url_https')

        self.client.db.feed.update_one(
            {
                'twitter_id': str(tweet.get('id')),
                'title': tweet.get('full_text'),
                'link': 'https://twitter.com/{}/status/{}'.format(
                    tweet.get('user').get('screen_name'),
                    tweet.get('id')
                ),
                'user': user_id,
                'media_url': media_url,
                "lang": tweet.get('metadata').get('iso_language_code')
            },
            {
                '$setOnInsert': {
                    'created_at': datetime.strptime(tweet.get('created_at'), '%a %b %d %X %z %Y'),
                    'validated': False,
                },
                '$set': self._set_counters(tweet)
            },
            upsert=True
        )

    def find_user_and_update_count(self, twitter_id):
        user_model = User()
        user = self.client.db.users.find_one({'twitter_id': twitter_id})
        user_twitter_id = user.get('twitter_id')
        tweets = self.find_by_user_twitter_id(user_tweeter_id=user_twitter_id)
        user_model.reset_counters_for_user(user_twitter_id)

        for tweet in tweets:
            self.update_user_count(user_tweeter_id=user_twitter_id, tweet=tweet)

    def update_user_count(self, user_tweeter_id, tweet):
        self.client.db.users.update_one(
            {'twitter_id': user_tweeter_id},
            {
                '$inc': self._set_counters(tweet)
            }
        )

    @staticmethod
    def _set_counters(tweet):
        return {
            'retweet_count': tweet.get('retweet_count'),
            'favorite_count': tweet.get('favorite_count')
        }
