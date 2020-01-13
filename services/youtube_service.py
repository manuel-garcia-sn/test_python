from datetime import datetime
from clients.youtube import YoutubeApi
from mongo_client import MongoClient
from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE, MONGODB_COLLECTION


class YoutubeService:
    @staticmethod
    def add_videos_to_feed():
        client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE,
            collection=MONGODB_COLLECTION
        )

        youtube_api = YoutubeApi()
        videos = youtube_api.videos()
        for video in videos:
            date = (video['snippet']['publishedAt'])[:-5]
            data = {
                'type': 'youtube',
                'internal_id': video['id']['videoId'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'link': 'https://www.youtube.com/watch?v={}'.format(video['id']['videoId']),
                'user': {
                    'name': video['snippet']['channelId'],
                    'screen_name': video['snippet']['channelTitle'],
                    'profile_image_url': video['snippet']['thumbnails']['default']['url']
                },
                'created_at': datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            }

            if client.collection.find_one({'type': 'youtube', 'internal_id': video['id']['videoId']}) is None:
                client.collection.insert_one(data)


y = YoutubeService()
y.add_videos_to_feed()

