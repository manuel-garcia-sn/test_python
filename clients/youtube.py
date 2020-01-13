import requests

from config.settings import YOUTUBE_SECRET


class YoutubeApi:
    def __init__(self, q):
        self.url = 'https://www.googleapis.com/youtube/v3/'
        self.token = ''
        self.q = q

    def videos(self):
        response = self._get_response()

        return response.json().get('items', {})

    def _get_response(self):
        payload = {
            'key': YOUTUBE_SECRET,
            'q': self.q,
            'type': 'video',
            'part': 'snippet'
        }
        response = requests.get('{}{}'.format(self.url, 'search'), params=payload)

        return response


y = YoutubeApi('sngularrocks')
y.videos()
