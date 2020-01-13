import pymongo

from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE, MONGODB_COLLECTION
from mongo_client import MongoClient


class Post:
    def __init__(self):
        self.client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE,
            collection=MONGODB_COLLECTION
        )

    def all(self, post_type=None):
        query = {}
        if post_type:
            query.update({'type': post_type})

        posts = self.client.collection.find(query, {'_id': False}).sort([('created_at', pymongo.DESCENDING)])

        return list(posts)
