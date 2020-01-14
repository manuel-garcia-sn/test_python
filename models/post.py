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
