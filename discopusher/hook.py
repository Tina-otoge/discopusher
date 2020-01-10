from discopusher import Config, push

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
        if self.config['type'] == 'twitter':
            from discopusher.handlers import TwitterHandler
            handler = TwitterHandler(self.name, app_config=self.app_config)
            for url in self.config['data']:
                content = handler.handle(url)
                for webhook in self.config['webhooks']:
                    push(content, webhook, self.config)
