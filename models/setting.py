import json
from datetime import datetime
import pymongo
from bson import ObjectId, json_util
from flask import Response

from models.base_model import BaseModel


class Setting(BaseModel):
    text_and_link_document = {
        'text_bold': '',
        'image': ''
    }

    settings_document = {
        'general': {
            'hashtag': '#SngularRocks!'
        },
        'opening': {
            'text_light': '',
            'text_bold': '',
            'background_resource': ''
        },
        'share': {
            'text_bold': '',
            'image': '',
            'left_text': '',
            'right_text': '',
            'show_more_text': ''
        },
        'have_fun': {
            'text_bold': '',
            'image': ''
        },
        'community': {
            'text_bold': '',
            'image': ''
        },
        'popular': {
            'text_bold': '',
            'image': ''
        },
        'join_us': {
            'text_light': '',
            'text_bold': '',
            'button_text': '',
            'slider_images': {

            }
        },
        'footer': {
            'follow_us': '',
            'links': {
                'facebook': '',
                'youtube': '',
                'instagram': '',
                'twitter': '',
                'linkedIn': ''
            }
        }
    }

    model = {
        'es': {
            'general': {
                'hashtag': '#SngularRocks!'
            },
            'opening': {
                'text_light': '',
                'text_bold': '',
                'background_resource': ''
            },
            'share': {
                'text_bold': '',
                'image': '',
                'left_text': '',
                'right_text': '',
                'show_more_text': ''
            },
            'have_fun': {
                'text_bold': '',
                'image': ''
            },
            'comunity': {
                'text_bold': '',
                'image': ''
            },
            'popular': {
                'text_bold': '',
                'image': ''
            },
            'join_us': {
                'text_light': '',
                'text_bold': '',
                'button_text': '',
                'slider_images': {

                }
            },
            'footer': {
                'follow_us': '',
                'links': {
                    'facebook': '',
                    'youtube': '',
                    'instagram': '',
                    'twitter': '',
                    'linkedIn': ''
                }
            }
        },
        'en': {
            'general': {
                'hashtag': '#SngularRocks!'
            },
            'opening': {
                'text_light': '',
                'text_bold': '',
                'background_resource': ''
            },
            'share': {
                'text_bold': '',
                'image': '',
                'left_text': '',
                'right_text': '',
                'show_more_text': ''
            },
            'have_fun': {
                'text_bold': '',
                'image': ''
            },
            'comunity': {
                'text_bold': '',
                'image': ''
            },
            'popular': {
                'text_bold': '',
                'image': ''
            },
            'join_us': {
                'text_light': '',
                'text_bold': '',
                'button_text': '',
                'slider_images': {

                }
            },
            'footer': {
                'follow_us': '',
                'links': {
                    'facebook': '',
                    'youtube': '',
                    'instagram': '',
                    'twitter': '',
                    'linkedIn': ''
                }
            }
        },
    }

    def __init__(self, collection='settings'):
        super().__init__(collection)

    def all(self):
        settings = self.client.db.settings.find()

        return list(settings)

    def store(self, settings):
        ##self.client.db.settings.drop()

        settings.update({'created_at': datetime.now()})

        self.client.db.settings.insert_one(
            settings
        )

        return settings
