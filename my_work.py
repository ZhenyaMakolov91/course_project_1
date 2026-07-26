import requests
from pprint import pprint


with open('vk_token.txt') as f:
    vk_token = f.read().strip()
#vk_token = input('Введите токен ВКонтакте: ')

with open('ya_token.txt') as f:
    ya_token = f.read().strip()
#ya_token = input('Введите токен Яндекс Диск:)

class VkUser:
    url = 'https://api.vk.ru/method/'

    def __init__(self, token, version):
        self.params = {'access_token': token, 'v': version}

    def photos_get(self, owner_id):
        '''получаем фотографии с профиля ВК по id'''
        url = self.url + 'photos.get/'
        params = {**self.params, 'owner_id': owner_id, 'album_id': 'profile', 'rev': 0, 'extended': 1, 'count': 10}
        req = requests.get(url=url, params=params)
        if req.status_code == 200:
            return req.json()
        print('Ошибка!')


class YaUpLoader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'QAuth {}'.format(self.token)
        }

    def upload_photos(self, file_path, name_photo):
        '''выгрузка фото на Яндекс Диск'''
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload/'
        params = {'path': f'{self.my_folder}/{name_photo}.jpeg', 'overwrite': 'true'}
        response1 = requests.get(url, headers=self.get_headers(), params=params).json()
        url = response1.get('href')  # получаем ссылку для загрузки файла
        with open(f'photos/{name_photo}.jpeg', 'wb') as f:
            response = requests.get(file_path)
            f.write(response.content)
        response2 = requests.put(url, open(f'photos/{name_photo}.jpeg', 'rb'))
        print('Готово!') if response2.status_code == 201 else print('Ошибка!')

    def new_folder_yadisk(self):
        '''создаем каталог на Яндекс Диск'''
        self.my_folder = input('Введите название для новой папки: ')
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers, params = self.get_headers(), {'path': self.my_folder}
        headers['Accept'] = 'application/json'
        req = requests.put(url, headers=headers, params=params)
        print('Папка создана!') if req.status_code == 201 else print('Ошибка!')


obj = VkUser(vk_token, '5.199')
my_photos = obj.photos_get('1')
print(my_photos)
# uploader = YaUpLoader(ya_token)
# uploader.new_folder_yadisk()

# for el in my_photos['response']['items']:
#     new_name = el['likes']['count']
#     url = el['sizes'][0]['url']
#     uploader.upload_photos(url, new_name)