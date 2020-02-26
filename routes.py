from flask import Blueprint, request, render_template

from views.posts import Posts, AddPostView
from views.users import Users
from views.settings import Settings
from models.setting import Setting
from models.post import Post
from models.user import User

api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/')
def hello_world():
    setting = Setting()
    post = Post()
    user = User()
    setting = setting.all()[-1]
    latest_ten_posts = post.all(q='sngularrocks')
    users = user.top_users()

    return render_template('index.html', setting=setting, posts=latest_ten_posts, users=users)


@api_routes.route('/test')
def show():
    return 'test'


@api_routes.route('/feed')
def feed():
    return Posts().list()


@api_routes.route('/users')
def users():
    return Users().list()


@api_routes.route('/settings', methods=['GET'])
def list_settings():
    return Settings().last_settings()


@api_routes.route('/settings', methods=['POST'])
def store_settings():
    return Settings().store(request.get_json())


@api_routes.route('/item/new', methods=['POST'])
def add_item():
    return AddPostView.perform_create()
