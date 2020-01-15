from clients.twitter import TwitterApi
from models.user import User
from models.post import Post


class TwitterService:
    def __init__(self):
        self.post = Post()
        self.user = User()
        self.post.drop_collection()
        self.user.drop_collection()

    def add_tweets_to_feed(self, query='sngularrocks'):
        tweets = self._get_tweets_from_api(query)

        for tweet in tweets:
            user_id = self.user.add_user(tweet=tweet)
            self.post.add_tweet_from_user(tweet=tweet, user_id=user_id)

    @staticmethod
    def _get_tweets_from_api(query):
        twitter_api = TwitterApi()
        tweets = twitter_api.tweets(query)

        return tweets


t = TwitterService()
t.add_tweets_to_feed()
