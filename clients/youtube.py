import sys
import settings
import requests

sys.path.append('../')


class YoutubeApi:
    def __init__(self):
        self.url = 'https://www.googleapis.com/youtube/v3/'
        self.token = ''

    def videos(self):
        response = self._get_response()

        return response.json().get('items', {})

    def _get_response(self):
        payload = {
            'key': settings.YOUTUBE_SECRET,
            'q': 'sngularrocks',
            'type': 'video',
            'part': 'snippet'
        }
        response = requests.get('{}search'.format(self.url), params=payload)

        return response


y = YoutubeApi()
y.videos()
