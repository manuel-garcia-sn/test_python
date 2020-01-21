import json

from bson import json_util
from flask import Response, request
from flask.views import View

from models.user import User


class Users:
    @staticmethod
    def list():
        validated = request.args.get('validated')
        users = User()

        return Response(json.dumps(users.all(validated), default=json_util.default), mimetype='application/json')

