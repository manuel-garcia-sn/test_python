import json

from bson import json_util
from flask import Response, request

from models.post import Post


class Posts:
    @staticmethod
    def list():
        post_type = request.args.get('type')
        query = request.args.get('q', 'sngularrocks')
        posts = Post()

        return Response(json.dumps(posts.all(query, post_type), default=json_util.default), mimetype='application/json')
