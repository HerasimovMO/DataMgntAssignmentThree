import re
import string

from mongo import Mongo
from mongo import Collection


def clean(item, collection: Collection):
    # https://docs.python.org/3/howto/regex.html

    if item[collection.content_field()] == None:
        print('FOUND NONE')
        return ''

    # remove all non-ascii characters
    text = item[collection.content_field()].encode(
        'ascii', 'ignore').decode('ascii')

    # remove all links, retweets, username mentions and news related characters
    main_re = r'http\S+|\[\+[0-9]{0,10} chars\]|[0-9]|(@[A-Za-z0-9]+)'
    text = re.sub(main_re, '', text, flags=re.IGNORECASE)

    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # remove double spaces
    text = re.sub(' +', ' ', text)

    return text.lower().strip()


def generate_file(text, file_name):
    file = open(f'{file_name}.txt', 'w')
    file.write(text)
    file.close()


mongo_db = Mongo(db_name='assignment_two')

tweets = " ".join(list(map(lambda x: clean(x, Collection.Tweets),
                           mongo_db.get_values(Collection.Tweets))))
print('Gethered and cleaned all the tweets')

news = " ".join(list(map(lambda x: clean(x, Collection.News),
                         mongo_db.get_values(Collection.News))))
print('Gethered and cleaned all the news')

content = re.sub(' +', ' ', (tweets + " " + news).replace('\n', ' '))
generate_file(content, 'content')
print('Generated text file with content of tweets and news')
