import os

from dotenv import load_dotenv

load_dotenv()

TWITTER_KEY = os.getenv('TWITTER_KEY')
TWITTER_SECRET = os.getenv('TWITTER_SECRET')
YOUTUBE_SECRET = os.getenv('YOUTUBE_SECRET')

MONGODB_HOST = os.getenv('MONGODB_HOST')
MONGODB_PORT = os.getenv('MONGODB_PORT')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION')
