import pymongo

import settings
from mongo_client import MongoClient


class Post:
    def __init__(self):
        self.client = MongoClient(
            host=settings.MONGODB_HOST,
            port=settings.MONGODB_PORT,
            db=settings.MONGODB_DATABASE,
            collection=settings.MONGODB_COLLECTION
        )

    def all(self, post_type):
        query = {}
        if post_type:
            query = {
                'type': post_type
            }

        posts = self.client.collection.find(query, {'_id': False}).sort([('created_at', pymongo.DESCENDING)])

        return list(posts)
