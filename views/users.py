import json

from bson import json_util
from flask import Response, request
from flask.views import View

from models.user import User


class Users:
    @staticmethod
    def list():
        validated = request.args.get('validated')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        users = User()

        return Response(json.dumps(users.all(q=search, page=page, validated=validated), default=json_util.default),
                        mimetype='application/json'
                        )
    @staticmethod
    def update():
        body_params = request.get_json()
        twitter_id = body_params.get('twitter_id')
        validated = body_params.get('validated')
        print(twitter_id)
        print(validated)
        users = User()

        users.enable_and_disable(twitter_id=twitter_id, validated=validated)

        return Response(json.dumps({}, default=json_util.default), status=201, mimetype='application/json')