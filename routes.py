import json

from flask import Blueprint, request, Response
from views.posts import Posts, AddPostView

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
    return AddPostView.perform_create()
