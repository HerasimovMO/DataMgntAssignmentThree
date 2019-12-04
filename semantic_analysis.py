from cleaner import Cleaner
from cleaner import Article
from mongo import Mongo
from mongo import Collection
from words_loader import WordsLoader

import enum
import csv

# keywords that we are looking for in tweets and news
keywords = ['University', 'Canada',
            'Dalhousie University', 'Halifax', 'Canada Education']

cleaner = Cleaner(db_name='assignment_three', collection=Collection.News)
articles = cleaner.get_articles()
print(articles[:5])
