import json

from bson import json_util
from flask import Blueprint, request, render_template, Response, send_from_directory

from views.posts import Posts, AddPostView
from views.users import Users
from views.settings import Settings
from models.setting import Setting
from models.post import Post
from models.user import User
from werkzeug.utils import secure_filename
import os

api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/')
def hello_world():
    setting = Setting()
    post = Post()
    user = User()
    settings = setting.all()

    settings_formatted = {}

    for element in settings:
        settings_formatted[element.get('name')] = element.get('data').get('es')

    latest_ten_posts = post.all(q='sngularrocks')
    users = user.top_users()

    return render_template('index.html', setting=settings_formatted, posts=latest_ten_posts, users=users)


@api_routes.route('/test')
def show():
    return 'test'


@api_routes.route('/feed')
def feed():
    return Posts().list()


@api_routes.route('/feed', methods=['POST'])
def update_feed():
    return Posts().enable_and_disable()


@api_routes.route('/users')
def users():
    return Users().list()


@api_routes.route('/users', methods=['POST'])
def update_user():
    return Users().update()


@api_routes.route('/settings', methods=['GET'])
def list_settings():
    return Settings().last_settings()


@api_routes.route('/settings', methods=['POST'])
def store_settings():
    return Settings().store(request.get_json())


@api_routes.route('/item/new', methods=['POST'])
def add_item():
    return AddPostView.perform_create()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@api_routes.route('/file-upload', methods=['POST'])
def upload_file():
    upload_folder = '/Users/manuel.garcia/PycharmProjects/untitled/uploads'

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return Response(json.dumps({'status': 'primer paso'}), status=400, mimetype='application/json')

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return Response(json.dumps({'status': 'segundo paso'}), status=400, mimetype='application/json')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))

            return Response(json.dumps({
                'file_name': filename,
                'path': os.path.join(upload_folder, filename),
                'short_path': 'uploads/' + filename
            }, default=json_util.default), status=201, mimetype='application/json')


@api_routes.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = '/Users/manuel.garcia/PycharmProjects/untitled/uploads'

    return send_from_directory(upload_folder, filename)
