import requests
from unittest import TestCase
import json


YA_TOKEN = ""
YA_DIR = "New_dir"
url = "https://cloud-api.yandex.net/v1/disk/resources"
params = {"path": YA_DIR}
headers = {"Authorization": f"OAuth {YA_TOKEN}"}


class TestYaDirUnitTest(TestCase):

    def test_dir_create_positive(self):
        # Добавление папки
        response = requests.put(url, params=params, headers=headers)
        # Проверка успешности
        self.assertEqual(response.status_code, 201)
        response = requests.get(url, params=params, headers=headers)
        item_type = json.loads(response.text)["type"]
        item_name = json.loads(response.text)["name"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item_type, "dir")
        self.assertEqual(item_name, YA_DIR)
        # Удаление папки
        response = requests.delete(url, params=params, headers=headers)
        # Проверка успешности
        self.assertEqual(response.status_code, 204)

    def test_dir_create_negative_already_exist(self):
        # Добавление папки
        response = requests.put(url, params=params, headers=headers)
        # Проверка успешности добавления
        self.assertEqual(response.status_code, 201)
        # Конфликт при попытке создания одноименной папки
        response = requests.put(url, params=params, headers=headers)
        self.assertEqual(response.status_code, 409)
        # Удаление папки
        response = requests.delete(url, params=params, headers=headers)
        # Проверка успешности
        self.assertEqual(response.status_code, 204)

    def test_dir_create_negative_unauthorized (self):
        # Попытка добавления папки без токена
        headers = {"Authorization": f"OAuth "}
        response = requests.put(url, params=params, headers=headers)
        # Unauthorized 
        self.assertEqual(response.status_code, 401)            
