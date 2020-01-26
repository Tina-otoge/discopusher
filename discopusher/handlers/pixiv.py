from pathlib import Path

from pixivpy3 import PixivAPI
import requests
from discopusher import Config

class PixivHandler:
    def __init__(self, name, app_config={}):
        config_path = Path(app_config.get('handlers_config_dir', '.')) / 'pixiv.toml'
        data_path = Path(app_config.get('data_dir', './data/')) / '{}.toml'.format(name)
        self.config = Config(config_path, write_defaults=True, defaults={
            'username': 'xxxx',
            'password': 'xxxx',
        })
        self.config.save()
        self.data = Config(data_path)
        self.age_filter = None
        self.api = PixivAPI()
        if self.config.get('password'):
            print('logging in to Pixiv...')
            login_response = self.api.login(self.config['username'], self.config['password'])
            print('logged in into account {0.name} ({0.account}) [{0.id}]'.format(login_response['response']['user']))

    def set_age_filter(self, filter):
        self.age_filter = filter

    def handle(self, feed):
        if feed == 'followings':
            data = self.api.me_following_works(image_sizes=['large'], include_stats=False)
        elif feed == 'bookmarks':
            data = self.api.me_favorite_works()
        else:
            return None, None
        if data['status'] != 'success':
            print('invalid response')
            print('got:')
            print(data)
            return None, None
        results = data['response']
        save_data = self.data.get(feed, {'last_id': 0})
        print('latest id: {}'.format(save_data.get('last_id')))
        results = list(filter(lambda x: x['id'] > save_data.get('last_id'), results))
        if len(results) == 0:
            return None, None
        save_data['last_id'] = results[0]['id']
        self.data[feed] = save_data
        self.data.save()
        ret = []
        for entry in results:
            print('Handling pixiv entry {}'.format(entry['id']))
            if self.age_filter != None:
                if entry['age_limit'] == 'r18' and self.age_filter == 'safe':
                    continue
                if entry['age_limit'] == 'all-age' and self.age_filter == 'r18':
                    continue
            content = '<https://www.pixiv.net/i/{}>'.format(entry['id'])
            content += '\n{} by {} ({})'.format(entry['title'], entry['user']['name'], entry['user']['account'])
            if entry['is_manga']:
                print('it\'s a manga')
                work = self.api.works(entry['id'])
                if work['status'] != 'success':
                    continue
                work = work['response']
                if len(work) == 0:
                    continue
                work = work[0]
                urls = [x['image_urls']['medium'] for x in work['metadata']['pages']]
                if len(urls) > 4:
                    content += '\n{} more pictures to not shown here'.format(len(urls) - 4)
                    urls = urls[:4]
            else:
                if entry['width'] > 2000 or entry['height'] > 2000:
                    content += '\n(not displaying full resolution because it is too large)'
                    urls = [entry['image_urls']['medium']]
                else:
                    urls = [entry['image_urls']['large']]
            files = []
            index = 0
            for url in urls:
                print('downloading picture...')
                response = requests.get(url, headers={'referer': 'https://pixiv.net'})
                if response.status_code != 200:
                    continue
                ext = Path(url).suffix
                files.append({'data': response.content, 'name': 'page{}.{}'.format(index, ext)})
                index += 1
            ret.append({'content': content, 'files': files})
        ret.reverse()
        return ret
