import settings
from pymongo import MongoClient as PymongoClient


class MongoClient:
    def __init__(self):
        self.client = PymongoClient('mongodb://' + settings.MONGODB_HOST + ':' + settings.MONGODB_PORT)
        self.db = self.client[settings.MONGODB_DATABASE]
        self.collection = self.db[settings.MONGODB_COLLECTION]