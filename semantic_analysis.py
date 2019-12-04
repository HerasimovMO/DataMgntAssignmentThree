from cleaner import Cleaner
from cleaner import Article
from mongo import Mongo
from mongo import Collection
from words_loader import WordsLoader

import csv
import functools
import math
import utility


class ArticleInfo:
    def __init__(self, article: Article, keywords):
        self.article = article
        self.keywords = keywords
        self.sentences = [article.title,
                          article.description,
                          article.content]

    def count_word(self, word):

        counts = list(map(lambda x: x.lower().count(
            word.lower()), self.sentences))
        return functools.reduce(lambda x, y: x + y, counts)

    def create_dict(self):
        info = {}

        for keyword in self.keywords:
            value = keyword.lower()
            count = self.count_word(value)
            info[value] = count

        info['total'] = len(' '.join(self.sentences).split())
        return info


def create_total_word_occurrences_table(keywords, counted_articles, file_name):
    total_word_occurrences_table = [
        ["Search Query", "Document containing term(df)", "Total Documents(N)/ number of documents term appeared (df)", "Log 10 (N/df)"]]

    for keyword in keywords:

        values = list(
            map(lambda x: 1 if x[keyword.lower()] > 0 else 0, counted_values))
        occurrences = functools.reduce(lambda x, y: x + y, values)

        tot_to_word_count = len(counted_values) / \
            occurrences if occurrences > 0 else 0
        log = math.log10(tot_to_word_count) if tot_to_word_count > 0 else 0

        info = [keyword, occurrences, tot_to_word_count, log]

        total_word_occurrences_table.append(info)

    utility.generate_file(total_word_occurrences_table, file_name)


def create_highest_occurrences_canada_table(counted_articles, file_name):
    word_occurrences_table = [
        ["Article number", "Total words", "Frequency"]]

    relative_frequencies = {}
    for (index, article) in enumerate(counted_articles):
        canada_occurrences = article['canada']
        if canada_occurrences > 0:
            info = [f'Article #{index}', article['total'], article['canada']]
            word_occurrences_table.append(info)
            relative_frequencies[index] = article['canada']/article['total']

    utility.generate_file(word_occurrences_table, file_name)
    return relative_frequencies


# keywords that we are looking for in tweets and news
keywords = ['University', 'Canada',
            'Dalhousie University', 'Halifax', 'Canada Education']

cleaner = Cleaner(db_name='assignment_three', collection=Collection.News)
articles = cleaner.get_articles()

counted_values = list(
    map(lambda x: ArticleInfo(x, keywords).create_dict(), articles))
print(
    f'Finished counting values. There are {len(counted_values)} news articles. Example {counted_values[:3]} ... \n')

first_file_name = 'number_of_documents_containing_keyword'
create_total_word_occurrences_table(
    keywords, counted_values, first_file_name)
print(
    f'Generated table that shows number of news articles where keywords appeared. Document is named {first_file_name}\n')

second_file_name = 'canada_occurrences_table'
relative_frequencies = create_highest_occurrences_canada_table(
    counted_values, second_file_name)
print(
    f'Generated table that shows news articles where word Canada appeared most. Document is named {second_file_name}\n')

(frequency, article_number) = max(
    zip(relative_frequencies.values(), relative_frequencies.keys()))
print(f'List of highest frequencies: {relative_frequencies}\n')
print(
    f'The highest relative frequency is {frequency}. The article number {article_number}, description: {articles[article_number]}')
