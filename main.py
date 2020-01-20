from flask import Flask
from routes import api_routes
from flask_script import Manager
from services.youtube_service import YoutubeService
from services.twitter_service import TwitterService

app = Flask(__name__)
app.register_blueprint(api_routes)

manager = Manager(app)


if __name__ == '__main__':
    manager.add_command('youtube_service', YoutubeService())
    manager.add_command('twitter_service', TwitterService())
    manager.run()
