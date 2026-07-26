import requests
from pprint import pprint
from json import dump


with open('vk_token.txt') as f:
    vk_token = f.read().strip()

with open('ya_token.txt') as f:
    ya_token = f.read().strip()

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
        self.token, self.added_photos = token, []

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
        with open(f'photos/{name_photo}.jpg', 'wb') as f:
            response = requests.get(file_path)
            f.write(response.content)
        response2 = requests.put(url, open(f'photos/{name_photo}.jpg', 'rb'))
        print('Успешно!') if response2.status_code == 201 else print('Ошибка!')

    def loads_photos_from_vk(self, photos, count=5):
        photos_list, count_result = [], 0
        for el in photos['response']['items']:
            count -= 1
            count_result += 1
            new_name = el['likes']['count']
            if new_name in self.added_photos:  # проверяем, что фото не совпадают по лайкам
                new_name = new_name + '_' + el['date']  # иначе в название добавим дату
            self.added_photos.append(new_name)
            largest_photo = max(el['sizes'], key=lambda x: x['type'])  # максимальный размер фото
            photos_list.append({'file_name': f'{new_name}.jpg', 'size': largest_photo['type']})
            self.upload_photos(largest_photo['url'], new_name)
            if not count:
                break
        print(f'Загружено фотографий количество фото: {count_result}')

        with open('data.json', 'w', encoding='utf-8') as file:
            dump(photos_list, file, indent=4, ensure_ascii=False)

    def new_folder_yadisk(self):
        '''создаем каталог на Яндекс Диск'''
        self.my_folder = input('Введите название для новой папки: ')
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers, params = self.get_headers(), {'path': self.my_folder}
        headers['Accept'] = 'application/json'
        req = requests.put(url, headers=headers, params=params)
        print('Папка создана!') if req.status_code == 201 else print('Ошибка!')


obj = VkUser(vk_token, '5.199')
# uploader = YaUpLoader(ya_token)
# uploader.new_folder_yadisk()
my_photos = obj.photos_get('1')
pprint(my_photos)
# uploader.loads_photos_from_vk(my_photos)