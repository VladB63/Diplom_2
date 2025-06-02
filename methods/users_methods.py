import allure
import requests
from data import UrlKey, CreateUsers

class UsersMethods:

    @allure.step('Создание уникального пользователя')
    def create_users(self):
        payload = {
            "email": CreateUsers.EMAIL,
            'password': CreateUsers.PASSWORD,
            'name': CreateUsers.NAME
        }
        response = requests.post(f'{UrlKey.BASE_URL}{UrlKey.REG_URL}', json=payload)
        return response.status_code, response.json()


    @allure.step('Создание пользователя с не полными данными')
    def create_user_fail(self, payload):
        response = requests.post(f'{UrlKey.BASE_URL}{UrlKey.REG_URL}', json=payload)
        return response.status_code, response.json()


    @allure.step('Логин под существующим пользователем')
    def log_user(self):
        payload = {
            'email': CreateUsers.EMAIL,
            'password': CreateUsers.PASSWORD
        }
        response = requests.post(f'{UrlKey.BASE_URL}{UrlKey.AUTH_URL}', json=payload)
        return response.status_code, response.json()


    @allure.step('Логин с не верным логином и паролем')
    def log_user_failed(self, payload):
        response = requests.post(f'{UrlKey.BASE_URL}{UrlKey.AUTH_URL}', json=payload)
        return response.status_code, response.json()


    @allure.step('Изменение данных')
    def change_user(self):
        payload = {
            'email': CreateUsers.EMAIL,
            'password': CreateUsers.PASSWORD
        }
        status_code, response = self.log_user()
        token = response.get('accessToken')
        headers = {"Authorization": token}
        response = requests.patch(f'{UrlKey.BASE_URL}{UrlKey.CHANGE_URL}', headers=headers, json=payload)
        return response.status_code, response.json()

    @allure.step('Изменение данных без авторизации')
    def change_user_fail(self):
        payload = {
            'email': CreateUsers.EMAIL,
            'password': CreateUsers.PASSWORD
        }
        response = requests.patch(f'{UrlKey.BASE_URL}{UrlKey.CHANGE_URL}', json=payload)
        return response.status_code, response.json()


    @allure.step('Удаление пользователя')
    def del_user(self):
        response = requests.delete(f'{UrlKey.BASE_URL}{UrlKey.CHANGE_URL}')
        return response.status_code, response.json()


