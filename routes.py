import json

from flask import Blueprint, request, Response
from views.posts import Posts

api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/')
def hello_world():
    return "Hello World!"


@api_routes.route('/test')
def show():
    return 'test'


@api_routes.route('/feed')
def feed():
    return Posts().list()


@api_routes.route('/item/new', methods=['POST'])
def add_item():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']

    # Add item to the list
    res_data = database_operations.add_to_list(item)

    if res_data is None:
        response = Response("{'error': 'Item not added - {}'}".format(item), status=400, mimetype='application/json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')

    return response
