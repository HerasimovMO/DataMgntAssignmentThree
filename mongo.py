# https://realpython.com/introduction-to-mongodb-and-python/#pymongo

from pymongo import MongoClient


class Mongo:
    def __init__(self, db_name):
        self.db_name = db_name
        self.client = MongoClient()
        self.db = self.client[self.db_name]

    def save_array(self, json_content, collection):
        self.db[collection].insert_many(json_content)

    def save_object(self, json_content, collection):
        self.db[collection].insert_one(json_content)
