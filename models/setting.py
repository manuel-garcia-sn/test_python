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

        self.client.db.settings.replace_one(
            {"name": settings.get('name')},
            settings,
            upsert=True
        )

        return settings
