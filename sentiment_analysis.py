from cleaner import Cleaner
from mongo import Mongo
from mongo import Collection


def generate_file(text, file_name):
    file = open(f'{file_name}.txt', 'w')
    file.write(text)
    file.close()


cleaner = Cleaner(db_name='assignment_three', collection=Collection.Tweets)
bags = cleaner.get_bag_of_words()

print(bags[0:5])
