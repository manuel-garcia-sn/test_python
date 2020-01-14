from datetime import datetime

from bson import ObjectId

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
            # create or update user
            twitter_user = tweet.get('user')
            found_user = client.db.users.find_one({
                'twitter_id': twitter_user.get('id')
            })

            if found_user is None:
                found_user = {
                    'twitter_id': twitter_user.get('id'),
                    'twitter_name': twitter_user.get('name'),
                    'retweet_count': 0,
                    'favorite_count': 0,
                    'validated': None
                }

                user_id = client.db.users.insert_one(found_user).inserted_id
                # print('user id si no existe el jambo', user_id)
            else:
                # print('YA EXISTE')
                user_id = found_user.get('_id')
                # print('user id si existe el jambo', user_id)

            # find_urls = (tweet.get('entities').get('urls'))
            #
            # urls = {}
            # if find_urls:
            #     urls = {
            #         'short_url': find_urls[0].get('url'),
            #         'expanded_url': find_urls[0].get('expanded_url'),
            #    }

            found_tweet = client.db.feed.find_one({'type': 'tweet', 'internal_id': tweet.get('id')})

            if found_tweet:
                update = {
                    'retweet_count': tweet.get('retweet_count'),
                    'favorite_count': tweet.get('favorite_count')
                }

                tweet_id = client.db.feed.update_one(
                    {'_id': ObjectId(found_tweet.get('_id'))},
                    {"$set": update},
                    upsert=False
                )

                print('updated:', found_tweet.get('_id'))

            else:
                data = {
                    'type': 'tweet',
                    'internal_id': tweet.get('id'),
                    'title': tweet.get('text'),
                    'link': 'https://twitter.com/{}/status/{}'.format(
                        tweet.get('user').get('screen_name'),
                        tweet.get('id')
                    ),
                    # 'urls': urls,
                    'retweet_count': tweet.get('retweet_count'),
                    'favorite_count': tweet.get('favorite_count'),
                    'user': user_id,
                    'created_at': datetime.strptime(tweet.get('created_at'), '%a %b %d %X %z %Y'),
                    'validated': None
                }

                tweet_id = client.db.feed.insert_one(data).inserted_id
                print('inserted:', tweet_id)

            # client.db.users.update_one(
            #     {'_id': ObjectId(user_id)},
            #     {'$push': {'tweets':  tweet_id}}
            # )


t = TwitterService()
t.add_tweets_to_feed()
