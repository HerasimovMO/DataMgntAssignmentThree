from cleaner import Cleaner
from mongo import Mongo
from mongo import Collection
from words_loader import WordsLoader

import enum
import csv


class Polarity(enum.Enum):
    Positive = 'positive'
    Negative = "negative"
    Neutral = 'neutral'


cleaner = Cleaner(db_name='assignment_three', collection=Collection.Tweets)
bags = cleaner.get_bag_of_words()

polarized_words = WordsLoader(
    file_name='words_with_polarity.txt').polarized_words


class PolarityInfo:
    def __init__(self, polarity, match, bag):
        if polarity > 0:
            self.polarity = Polarity.Positive
        elif polarity == 0:
            self.polarity = Polarity.Neutral
        elif polarity < 0:
            self.polarity = Polarity.Negative

        self.polarity_value = polarity
        self.match = " ".join(match)
        self.coverage = len(match) / len(bag)
        self.match_count = len(match)

    def convert_to_array(self):
        return [self.polarity.value, self.polarity_value, self.match, self.match_count, self.coverage * 100]

    def __repr__(self):
        return f'polarity = {self.polarity.value}; polarity value = {self.polarity_value}; match = {self.match}; match length = {self.match_count} words; coverage = {self.coverage * 100}%'


def identify_polarity(bag):
    match = []
    tweet_polarity = 0
    for (key, value) in bag.items():
        # print(f'The key is {key} and the value is {value}')
        if key in polarized_words:
            tweet_polarity += (float(polarized_words[key]) * value)
            match.append(key)
    return PolarityInfo(tweet_polarity, match, bag)


def generate_file(data, file_name):

    with open(file_name + '.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    file.close()


data = [['polarity', 'polarity value', 'match',
         'match length (words)', 'coverage (%)']]

for bag in bags[:600]:
    polarity_info = identify_polarity(bag)
    print('Finished polarization')
    data.append(polarity_info.convert_to_array())

generate_file(data, 'polarized_tweets')
print('File generated')
