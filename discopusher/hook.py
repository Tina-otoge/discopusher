from discord_webhook import DiscordWebhook

from discopusher import Config

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

    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__,
            self.name
        )

    def push(self, content, webhook, files=[]):
        if isinstance(content, str):
            content = [content]
        webhook = DiscordWebhook(url=webhook)
        webhook.avatar_url = self.config.get('avatar_url')
        webhook.username = self.config.get('username')
        for file in files:
            webhook.add_file(file=file['data'], filename=file['name'])
        for msg in content:
            webhook.content = msg
            webhook.execute()

    def handle(self):
        if self.config['type'] == 'twitter':
            from discopusher.handlers import TwitterHandler
            handler = TwitterHandler(self.name, app_config=self.app_config)
            for url in self.config['data']:
                content = handler.handle(url)
                self.push(content, self.config['webhooks'])
        if self.config['type'] == 'pixiv':
            from discopusher.handlers import PixivHandler
            handler = PixivHandler(self.name, app_config=self.app_config)
            handler.set_age_filter(self.config.get('age_filter'))
            feed = self.config.get('feed')
            results = handler.handle(feed)
            for result in results:
                if result is None:
                    continue
                self.push(result['content'], self.config['webhooks'], files=result['files'])
