from clients.twitter import TwitterApi
from models.user import User
from models.post import Post
from flask_script import Command


class TwitterService(Command):
    def __init__(self):
        super().__init__()
        self.post = Post()
        self.user = User()

    def run(self, query='sngularrocks'):
        ## Añadir en la query exclude:replies exclude:retweets para omitir los retweets y las respuestas
        query += ' exclude:replies exclude:retweets'
        tweets = self._get_tweets_from_api(query)

        for tweet in tweets:
            user_id = self.user.add_user(tweet=tweet)
            self.post.add_tweet_from_user(tweet=tweet, user_id=user_id)

    @staticmethod
    def _get_tweets_from_api(query):
        twitter_api = TwitterApi()
        tweets = twitter_api.tweets(query)

        return tweets
