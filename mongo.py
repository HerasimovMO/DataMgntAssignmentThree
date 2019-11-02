# https://realpython.com/introduction-to-mongodb-and-python/#pymongo

from pymongo import MongoClient
import enum


class Collection(enum.Enum):
    Tweets = "tweets"
    News = "news"

    def content_field(self):
        return 'text' if self == Collection.Tweets else 'description'


class Mongo:
    def __init__(self, db_name):
        self.db_name = db_name
        self.client = MongoClient()
        self.db = self.client[self.db_name]

    def save_array(self, json_content, collection):
        self.db[collection].insert_many(json_content)

    def save_object(self, json_content, collection):
        self.db[collection].insert_one(json_content)

    def get_values(self, collection: Collection):
        return self.db[collection.value].find({}, {collection.content_field(): 1, '_id': 0})
