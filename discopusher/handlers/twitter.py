from pathlib import Path

import twitter

from discopusher import Config

class TwitterHandler:
    def __init__(self, name, app_config={}):
        config_path = Path(app_config.get('handlers_config_dir', '.')) / 'twitter.toml'
        data_path = Path(app_config.get('data_dir', './data/')) / '{}.toml'.format(name)
        self.config = Config(config_path, write_defaults=True, defaults={
            'consumer': 'xxxx',
            'consumer_secret': 'xxxx',
            'access': 'xxxx',
            'access_secret': 'xxxx',
        })
        self.config.save()
        self.data = Config(data_path)
        self.api = twitter.Api(
            consumer_key=self.config['consumer'],
            consumer_secret=self.config['consumer_secret'],
            access_token_key=self.config['access'],
            access_token_secret=self.config['access_secret']
        )

    def get_type(self, url):
        if '/search?' in url:
            return 'search'
        return None

    def get_name(self, url, type=None):
        type = type or self.get_type(url)
        if type == 'search':
            return self.get_search_term(url)

    def get_search_term(self, url):
        return url[url.find('q=')+2:url.rfind('&')]

    def handle(self, url):
        type = self.get_type(url)
        name = self.get_name(url, type=type)
        data = self.data.get(name, {'last_id': 0})
        print('last id:', data['last_id'])
        if type == 'search':
            results = self.api.GetSearch(
                raw_query='q={}'.format(name),
                since_id=data['last_id'],
                count=100,
                result_type='recent',
            )
        else:
            results = []
        results = list(filter(lambda x: x.id > data['last_id'], results))
        if results:
            data['last_id'] = results[0].id
        self.data[name] = data
        self.data.save()
        return [
            'https://twitter.com/{0.user.screen_name}/status/{0.id}'.format(tweet)
            for tweet in results
        ]

