from news import NewsLoader
from mongo import Mongo
from mongo import Collection
from tweets import TwitterStream
from tweets import TwitterSearch

mongo_db = Mongo(db_name='assignment_two')

keywords = ['University', 'Canada',
            'Dalhousie University', 'Halifax', 'Canada Education']

news = NewsLoader(keywords)
mongo_db.save_array(news.load_news(), Collection.News)
print('SUCCESS: Collected news articles')

print('Started streaming tweets')
twitter_stream = TwitterStream(keywords=keywords,
                               mongo=mongo_db,
                               collection=Collection.Tweets)
twitter_stream.start()

# twitter_search = TwitterSearch()
# mongo_db.save_array(twitter_search.search(keywords), Collection.Tweets)
