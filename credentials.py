from tweepy import OAuthHandler


class TwitterAuth:

    def create(self):
        access_token = '4064339116-j9Zbm9nixk9bbG4m2YHmuRUwQyp6tNSApRlbRI3'
        access_token_secret = 'AljmkUMGgyNFajjjk5dXesAhF8UNVmJS7ykhL8NMBd30S'
        api_key = 'e8sHJUKlUuJ06P91Zh0TSpjJ3'
        api_secret = '6wY8BTNIThDGm3hDbKGWekmAWjT2XbnJtywE6WcPjRicxoqI3Y'

        auth = OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth


class News:
    api_key = '1a7cca10b45b4f0b959bfa6311ace65f'
