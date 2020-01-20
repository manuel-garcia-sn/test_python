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
        print('counters back to 0')
        for user in self.user.all():
            user_id = user.get('_id')
            tweets = self.post.find_by_user_id(user_id=user_id)
            self._process_user_tweets(user_id=user_id, tweets=tweets)

    def _process_user_tweets(self, user_id, tweets):
        for tweet in tweets:
            self.post.update_user_count(user_id=user_id, tweet=tweet)
