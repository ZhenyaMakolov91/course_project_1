import requests
from pprint import pprint


with open('token.txt') as file_object:
    token = file_object.read().strip()


class VkUser:
    url = 'https://api.vk.ru/method/'

    def __init__(self, token, version):
        self.params = {'access_token': token, 'v': version}

    def photos_get(self, owner_id):
        url = self.url + 'photos.get/'
        params = {**self.params, 'owner_id': owner_id, 'album_id': 'profile', 'rev': 0, 'extended': 1, 'count': 10}
        req = requests.get(url, params).json()
        return req


obj = VkUser(token, '5.199')
pprint(obj.photos_get('1'))