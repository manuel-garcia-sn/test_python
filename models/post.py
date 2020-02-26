from datetime import datetime
import pymongo
from bson import ObjectId

from models.base_model import BaseModel


class Post(BaseModel):
    def __init__(self, collection='feed'):
        super().__init__(collection)

    def all(self, q, post_type=None):
        query = {'$text': {'$search': q}}
        if post_type:
            query.update({'type': post_type})

        posts = self.client.db.feed.find(query, {'_id': False}).sort([('created_at', pymongo.DESCENDING)])

        return list(posts)

    def find_by_user_id(self, user_id):
        return self.client.db.feed.find({'user': ObjectId(user_id)})

    def find_by_user_twitter_id(self, user_tweeter_id):
        return self.client.db.feed.find({'user.profile.twitter_id': user_tweeter_id})

    def add_tweet_from_user(self, tweet, user_id):
        media_url = ''
        if tweet.get('entities').get('media') is not None:
            media_url = tweet.get('entities').get('media')[0].get('media_url_https')

        self.client.db.feed.update_one(
            {
                'twitter_id': tweet.get('id'),
                'title': tweet.get('text'),
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
