import json

from bson import json_util
from flask import request, Response
from flask.views import View

from models.post import Post


class Posts:
    @staticmethod
    def list():
        post_type = request.args.get('type')
        page = int(request.args.get('page', 0))
        query = request.args.get('q', 'sngularrocks')
        posts = Post()

        return Response(json.dumps(posts.all(query, page, post_type), default=json_util.default), mimetype='application/json')


class AddPostView(View):
    @staticmethod
    def perform_create():
        try:
            req_data = request.get_json()
        except:
            return Response(
                json.dumps({'error': 'Cannot create post. Post info is missing'}),
                status=400,
                mimetype='application/json'
            )

        item = req_data.get('item')
        post = Post()
        res_data = post.client.db.feed.insert_one({'item': item})

        if res_data is None:
            response = Response(json.dumps({'error': 'Item not added - {}'}), status=400, mimetype='application/json')
            return response

        response = Response(response=None, status=201, mimetype='application/json')

        return response
