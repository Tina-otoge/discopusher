from pixivpy3 import PixivAPI
import json

api = PixivAPI()
api.login('shookaite@gmail.com', 'SQarX9pb')
# data = api.works(79102155)
data = api.me_following_works()
with open('sample_following.json', 'w') as f:
    json.dump(data, f, indent=4)
