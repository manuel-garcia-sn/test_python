import settings
import requests
import datetime
from mongo_client import MongoClient


class YoutubeApi:
    def __init__(self):
        self.url = 'https://www.googleapis.com/youtube/v3/'
        self.token = ''

    def get_videos(self):
        response = self.get_response_from_youtube()
        client = MongoClient()

        for video in response.json()['items']:
            date = (video['snippet']['publishedAt'])[:-5]
            data = {
                'type': 'youtube',
                'internal_id': video['id']['videoId'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'link': 'https://www.youtube.com/watch?v=' + video['id']['videoId'],
                'user': {
                    'name': video['snippet']['channelId'],
                    'screen_name': video['snippet']['channelTitle'],
                    'profile_image_url': video['snippet']['thumbnails']['default']['url']
                },
                'created_at': datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            }

            if client.collection.find_one({'type': 'youtube', 'internal_id': video['id']['videoId']}) is None:
                client.collection.insert_one(data)

        return response.json()['items']

    def get_response_from_youtube(self):
        payload = {
            'key': settings.YOUTUBE_SECRET,
            'q': 'sngularrocks',
            'type': 'video',
            'part': 'snippet'
        }
        response = requests.get(self.url + 'search', params=payload)
        print(response.status_code)

        return response


y = YoutubeApi()
y.get_videos()
