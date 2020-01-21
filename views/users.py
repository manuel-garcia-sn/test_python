import json

from bson import json_util
from flask import Response
from flask.views import View

from models.user import User


class Users:
    @staticmethod
    def list():
        # connect to model and return all users
        users = User()

        return Response(json.dumps(users.all(), default=json_util.default), mimetype='application/json')

