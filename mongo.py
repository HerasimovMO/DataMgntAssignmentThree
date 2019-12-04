# REFERENCE
#
# Real Python, “Introduction to MongoDB and Python,” Real Python, 08-Jul-2019. [Online].
# Available: https://realpython.com/introduction-to-mongodb-and-python/#pymongo. [Accessed: 05-Nov-2019].

from pymongo import MongoClient
import enum


class Collection(enum.Enum):
    Tweets = "tweets"
    News = "news"

    def content_field(self):
        return ['text'] if self == Collection.Tweets else ['title', 'description', 'content']


class Mongo:
    def __init__(self, db_name):
        self.db_name = db_name
        self.client = MongoClient()
        self.db = self.client[self.db_name]

    def get_values(self, collection: Collection):
        fields = collection.content_field()
        retrieve_fields = {'_id': 0}
        for field in fields:
            retrieve_fields[field] = 1

        return self.db[collection.value].find({}, retrieve_fields)
