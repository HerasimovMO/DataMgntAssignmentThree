import re
import string

from mongo import Collection
from mongo import Mongo


class Cleaner:
    def __init__(self, db_name, collection: Collection):

        # create mongo instance
        mongo_db = Mongo(db_name)
        self.collection = collection
        self.items = mongo_db.get_values(collection)

    def get_bag_of_words(self):
        return list(map(lambda x: self.clean_and_count(x), self.items))

    def create_bag(self, text):
        words = text.split(" ")
        bag = {}

        for word in words:
            if word in bag:
                bag[word] += 1
            else:
                bag[word] = 1
        return bag

    def clean_and_count(self, item):

        # “Regular Expression,” Regular Expression - Python 3.8.0 documentation. [Online].
        # Available: https://docs.python.org/3/howto/regex.html. [Accessed: 05-Nov-2019].
        if item[self.collection.content_field()] == None:
            print('FOUND NONE')
            return ''

        # A. Adam, "Removing emojis from a string in Python", Stack Overflow, 2019. [Online].
        # Available: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python. [Accessed: 06- Nov- 2019].
        # remove all non-ascii characters
        text = item[self.collection.content_field()].encode(
            'ascii', 'ignore').decode('ascii')

        # remove all links, retweets, username mentions and news related characters
        main_re = r'http\S+|\[\+[0-9]{0,10} chars\]|[0-9]|(@[A-Za-z0-9]+)'
        text = re.sub(main_re, '', text, flags=re.IGNORECASE)

        # L. J. L. Johnston, “Best way to strip punctuation from a string,” Stack Overflow, 01-Jan-1959. [Online].
        # Available: https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string. [Accessed: 05-Nov-2019].
        # remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        # remove double spaces
        text = re.sub(' +', ' ', text)

        return self.create_bag(text.lower().strip())
