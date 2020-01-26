from discord_webhook import DiscordWebhook

from discopusher import Config
from discopusher.push import push

class Hook:
    def __init__(self, path, app_config={}):
        self.app_config = app_config
        self.path = path
        self.name = path.stem
        self.config = Config(path, write_defaults=True, defaults={
            'type': 'twitter',
            'data': [],
            'webhooks': []
        })
        self.config.save()
        self.type = self.config.get('type')

    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__,
            self.name
        )

    def handle(self):
        print('handling {}'.format(self))
        if self.config['type'] == 'twitter':
            from discopusher.handlers import TwitterHandler
            handler = TwitterHandler(self.name, app_config=self.app_config)
            for url in self.config['data']:
                content = handler.handle(url)
                push(content, self.config['webhooks'], self.config)
        if self.config['type'] == 'pixiv':
            from discopusher.handlers import PixivHandler
            handler = PixivHandler(self.name, app_config=self.app_config)
            handler.set_age_filter(self.config.get('age_filter'))
            feed = self.config.get('feed')
            results = handler.handle(feed)
            for result in results:
                if result is None:
                    continue
                push(result['content'], self.config['webhooks'], self.config, files=result['files'])
