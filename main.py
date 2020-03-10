from flask import Flask

from routes import api_routes
from flask_script import Manager
from flask_cors import CORS

from services.count_service import CountService
from services.youtube_service import YoutubeService
from services.twitter_service import TwitterService

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_routes)

manager = Manager(app)


if __name__ == '__main__':
    manager.add_command('youtube_service', YoutubeService())
    manager.add_command('twitter_service', TwitterService())
    manager.add_command('count_service', CountService())
    manager.run()
