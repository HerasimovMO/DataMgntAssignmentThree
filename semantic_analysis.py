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

    def count_word(self, word):
        sentences = [self.article.title,
                     self.article.description,
                     self.article.content]

        counts = list(map(lambda x: x.lower().count(word.lower()), sentences))
        return functools.reduce(lambda x, y: x + y, counts)

    def create_dict(self):
        info = {}

        for keyword in self.keywords:
            value = keyword.lower()
            count = self.count_word(value)
            info[value] = count

        return info


# keywords that we are looking for in tweets and news
keywords = ['University', 'Canada',
            'Dalhousie University', 'Halifax', 'Canada Education']

cleaner = Cleaner(db_name='assignment_three', collection=Collection.News)
articles = cleaner.get_articles()

counted_values = list(map(lambda x: ArticleInfo(
    x, keywords).create_dict(), articles))

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

utility.generate_file(total_word_occurrences_table,
                      'number_of_documents_containing_keyword')
