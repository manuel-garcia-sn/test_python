from datetime import datetime
from clients.twitter import TwitterApi
from mongo_client import MongoClient
from config.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE


class TwitterService:
    @staticmethod
    def add_tweets_to_feed(query='sngularrocks'):
        client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            db=MONGODB_DATABASE
        )

        twitter_api = TwitterApi()
        tweets = twitter_api.tweets(query)

        for tweet in tweets:
            find_urls = (tweet.get('entities').get('urls'))

            urls = {}
            if find_urls:
                urls = {
                    'short_url': find_urls[0].get('url'),
                    'expanded_url': find_urls[0].get('expanded_url'),
                }

            user = tweet.get('user')

            tweet = client.db.feed.find_one({'type': 'tweet', 'internal_id': tweet.get('id')})

            if tweet:
                tweet.update('retweet_count', tweet.get('retweet_count'))
                tweet.update('favorite_count', tweet.get('favorite_count'))

                update = {
                    'retweet_count': tweet.get('retweet_count'),
                    'favorite_count': tweet.get('favorite_count')
                }

                client.db.feed.update_one({'_id': tweet.get('_id')}, {"$set": update}, upsert=False)

            # data = {
            #     'type': 'tweet',
            #     'internal_id': tweet.get('id'),
            #     'title': tweet.get('text'),
            #     'link': 'https://twitter.com/{}/status/{}'.format(
            #         tweet.get('user').get('screen_name'),
            #         tweet.get('id')
            #     ),
            #     'urls': urls,
            #     'retweet_count': tweet.get('retweet_count'),
            #     'favorite_count': tweet.get('favorite_count'),
            #     'user': {
            #         'name': user.get('name'),
            #         'screen_name': user.get('screen_name'),
            #         'profile_image_url': user.get('profile_image_url_https')
            #     },
            #     'created_at': datetime.strptime(tweet.get('created_at'), '%a %b %d %X %z %Y')
            # }
            #
            # if tweet is None:
            #     client.db.feed.insert_one(data)


t = TwitterService()
t.add_tweets_to_feed()
