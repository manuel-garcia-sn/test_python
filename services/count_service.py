from datetime import datetime

from bson import ObjectId

from clients.twitter import TwitterApi
from mongo_client import MongoClient
from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE


class CountService:
    @staticmethod
    def calculate_count():
        client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE
        )

        users = client.db.users.find({})

        for user in users:
            tweets = client.db.feed.find({'_id': ObjectId(user.get('_id'))})

            for tweet in tweets:
                #TODO: calcular el total de counts fav + rt y actualizar el count en el documento del usuario


c = CountService()
c.calculate_count()
