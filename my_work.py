import requests
from pprint import pprint


with open('token.txt') as file_object:
    token = file_object.read().strip()


class VkUser:
    url = 'https://api.vk.ru/method/'

    def __init__(self):
        pass