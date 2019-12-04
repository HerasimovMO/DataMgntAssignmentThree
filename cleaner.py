import re
import string

from mongo import Mongo
from mongo import Collection


def clean(item, collection: Collection):
    # “Regular Expression,” Regular Expression - Python 3.8.0 documentation. [Online].
    # Available: https://docs.python.org/3/howto/regex.html. [Accessed: 05-Nov-2019].

    if item[collection.content_field()] == None:
        print('FOUND NONE')
        return ''

    # A. Adam, "Removing emojis from a string in Python", Stack Overflow, 2019. [Online].
    # Available: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python. [Accessed: 06- Nov- 2019].
    # remove all non-ascii characters
    text = item[collection.content_field()].encode(
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

    return text.lower().strip()


def generate_file(text, file_name):
    file = open(f'{file_name}.txt', 'w')
    file.write(text)
    file.close()


# create mongo instance
mongo_db = Mongo(db_name='assignment_three')

# load tweets from database and clean the content
tweets = list(map(lambda x: clean(x, Collection.Tweets),
                  mongo_db.get_values(Collection.Tweets)))
print('Gethered and cleaned all the tweets')

print(tweets[0])
