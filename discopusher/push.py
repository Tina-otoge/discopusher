from discord_webhook import DiscordWebhook

def push(self, content, webhook, options={}, files=[]):
    if isinstance(content, str):
        content = [content]
    webhook = DiscordWebhook(url=webhook)
    webhook.avatar_url = options.get('avatar_url')
    webhook.username = options.get('username')
    for file in files:
        webhook.add_file(file=file['data'], filename=file['name'])
    for msg in content:
        webhook.content = msg
        webhook.execute()
