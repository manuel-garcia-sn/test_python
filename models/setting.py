import json
from datetime import datetime
import pymongo
from bson import ObjectId, json_util
from flask import Response

from models.base_model import BaseModel


class Setting(BaseModel):
    def __init__(self, collection='settings'):
        super().__init__(collection)

    def all(self, section=None):
        query = {}
        if section:
            query.update({'name': section})

        settings = self.client.db.settings.find(query)

        return list(settings)

    def store(self, settings):
        settings.update({'created_at': datetime.now()})
        key_to_update = "data"
        if settings.get('lang'):
            key_to_update = (key_to_update + ".{}").format(settings.get('lang'))

        self.client.db.settings.update_one(
            {"name": settings.get('name')},
            {'$set': {key_to_update: settings.get('data')}},
            upsert=True
        )

        return settings
