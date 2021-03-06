from models.post import Post
from models.user import User
from flask_script import Command


class CountService(Command):
    def __init__(self):
        super().__init__()
        self.user = User()
        self.post = Post()

    def run(self):
        self.user.reset_counters()
        for user in self.user.all():
            user_twitter_id = user.get('twitter_id')
            tweets = self.post.find_by_user_twitter_id(user_tweeter_id=user_twitter_id)
            self._process_user_tweets(user_twitter_id=user_twitter_id, tweets=tweets)

    def _process_user_tweets(self, user_twitter_id, tweets):
        for tweet in tweets:
            self.post.update_user_count(user_tweeter_id=user_twitter_id, tweet=tweet)
