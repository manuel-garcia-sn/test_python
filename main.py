from flask import Flask

from routes import api_routes
from flask_script import Manager
from flask_cors import CORS

from services.count_service import CountService
from services.youtube_service import YoutubeService
from services.twitter_service import TwitterService

app = Flask(__name__)
app.register_blueprint(api_routes)
app.secret_key = '76d78f6asdf8sd76f'
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app, resources={r'/*': {"origins": '*'}})

manager = Manager(app)


if __name__ == '__main__':
    manager.add_command('youtube_service', YoutubeService())
    manager.add_command('twitter_service', TwitterService())
    manager.add_command('count_service', CountService())
    manager.run()
