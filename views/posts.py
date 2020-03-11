import json

from bson import json_util
from flask import request, Response
from flask.views import View

from models.post import Post

class Posts:
    @staticmethod
    def list():
        post_type = request.args.get('type')
        page = int(request.args.get('page', 1))
        query = request.args.get('q', 'sngularrocks')
        posts = Post()

        return Response(json.dumps(posts.all(query, page, post_type), default=json_util.default),
                        mimetype='application/json')

    @staticmethod
    def enable_and_disable():
        post = Post()
        request_data = request.get_json()

        post.client.db.feed.update_one(
            {"twitter_id": request_data.get('twitter_id')},
            {'$set': {'validated': request_data.get('validated')}},
        )

        post_object = post.client.db.feed.find_one({"twitter_id": request_data.get('twitter_id')})
        twitter_id = post_object.get('user').get('profile').get('twitter_id')

        post.find_user_and_update_count(twitter_id)

        return Response(json.dumps(
            post_object,
            default=json_util.default),
            status=201,
            mimetype='application/json'
        )


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
