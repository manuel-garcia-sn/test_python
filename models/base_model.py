from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
from mongo_client import MongoClient


class BaseModel:
    def __init__(self, collection):
        self.client = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT, db=MONGODB_DATABASE)
        self.collection = collection

    def drop_collection(self):
        self.client.db[self.collection].drop()
