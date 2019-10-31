import requests

from credentials import News


class NewsLoader:
    def __init__(self, keywords):
        self.keywords = keywords

    def construct_request(self):
        base = 'https://newsapi.org/'
        path = 'v2/everything'
        q = "OR".join(list(map(lambda x: f'(+{x})', self.keywords)))

        self.url = base + path
        self.parameters = {
            'q': q,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': '100'
        }
        self.headers = {'X-Api-Key': News.api_key}

    def load_news(self):
        self.construct_request()

        resp = requests.get(url=self.url, params=self.parameters,
                            headers=self.headers)
        return resp.json()['articles']
