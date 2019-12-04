from mongo import Mongo
from mongo import Collection

mongo_db = Mongo(db_name='assignment_three')

# keywords that we are looking for in tweets and news
keywords = ['University', 'Canada',
            'Dalhousie University', 'Halifax', 'Canada Education']
