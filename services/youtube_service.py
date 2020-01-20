from datetime import datetime
from clients.youtube import YoutubeApi
from mongo_client import MongoClient
from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE


class YoutubeService:
    @staticmethod
    def add_videos_to_feed(query='sngularrocks'):
        client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE
        )

        youtube_api = YoutubeApi(query)
        videos = youtube_api.videos()
        for video in videos:
            video_id = video.get('id').get('videoId')
            snippet = video.get('snippet')
            date = (video.get('snippet').get('publishedAt'))[:-5]

            data = {
                'type': 'youtube',
                'internal_id': video_id,
                'title': snippet.get('title'),
                'description': snippet.get('description'),
                'link': '{}?v={}'.format('https://www.youtube.com/watch', video_id),
                'user': {
                    'name': snippet.get('channelId'),
                    'screen_name': snippet.get('channelName'),
                    'profile_image_url': snippet.get('thumbnails').get('default').get('url')
                },
                'created_at': datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            }

            if client.db.feed.find_one({'type': 'youtube', 'internal_id': video_id}) is None:
                client.db.feed.insert_one(data)


if __name__ == 'main':
    y = YoutubeService()
    y.add_videos_to_feed()
