import requests

def push(content, webhook, options={}):
    if isinstance(content, str):
        content = [content]
    for msg in content:
        requests.post(webhook, json={
            'content': msg,
            'avatar_url': options.get('avatar_url'),
            'username': options.get('username'),
        })
