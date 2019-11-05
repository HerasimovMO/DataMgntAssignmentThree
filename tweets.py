# “Streaming With Tweepy” Streaming With Tweepy - tweepy 3.8.0 documentation. [Online].
# Available: https://tweepy.readthedocs.io/en/latest/streaming_how_to.html. [Accessed: 05-Nov-2019].

import tweepy

from tweepy import Stream
from tweepy import StreamListener
from credentials import TwitterAuth
from mongo import Mongo
from mongo import Collection

auth = TwitterAuth().create()


class Tweet(object):
    def __init__(self, status):
        self.id = status.id_str
        self.text = status.text.strip()
        self.source = status.source
        self.source_url = status.source_url
        self.created_at = status._json['created_at']
        self.language = status.lang
        self.author_sreen_name = status.author.screen_name
        self.author_name = status.author.name

# used for searching tweets


class TwitterSearch:
    def search(self, keywords):
        api = tweepy.API(auth)
        query = "OR".join(list(map(lambda x: f'(+{x})', keywords)))

        public_tweets = api.search(query, result_type='mixed', count=100)
        tweets = list(map(lambda x: Tweet(x).__dict__, public_tweets))

        # take a look at Cursor
        print(f'Number of tweets is {len(public_tweets)}')
        return tweets

# used for streaming tweets


class TwitterStream:
    class EducationStreamListner(StreamListener):
        def __init__(self, mongo: Mongo, collection):
            StreamListener.__init__(self)

            self.counter = 0
            self.mongo = mongo
            self.collection = collection

        def on_status(self, status):
            tweet = Tweet(status).__dict__
            self.mongo.save_object(tweet, collection=self.collection)

            self.counter = self.counter + 1
            print(f"Downloaded number of tweets {self.counter}")

        def on_error(self, status_code):
            if status_code == 420:
                # returning False in on_error disconnects the stream
                return False

    def __init__(self, keywords, mongo, collection: Collection):
        self.keywords = keywords

        new_stream = TwitterStream.EducationStreamListner(mongo, collection)
        self.stream = Stream(auth=auth, listener=new_stream)

    def start(self):
        self.stream.filter(track=self.keywords)
