from models.post import Post
from models.user import User


class CountService:
    def __init__(self):
        self.user = User()
        self.post = Post()

    def calculate(self):
        self.user.reset_counters()
        print('counters back to 0')
        for user in self.user.all():
            user_id = user.get('_id')
            tweets = self.post.find_by_user_id(user_id=user_id)
            self._process_user_tweets(user_id=user_id, tweets=tweets)

    def _process_user_tweets(self, user_id, tweets):
        for tweet in tweets:
            self.post.update_user_count(user_id=user_id, tweet=tweet)


if __name__ == '__main__':
    c = CountService()
    c.calculate()
