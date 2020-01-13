from pymongo import MongoClient as PymongoClient


class MongoClient:
    def __init__(self, host, port, db):
        self.client = PymongoClient('mongodb://{}:{}'.format(host, port))
        self.db = self.client[db]

        self.db.feed.create_index([('title', 'text')])