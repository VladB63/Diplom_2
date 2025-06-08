import allure
import requests
from data import UrlKey


class OrderMethods:

    @allure.step('Создание заказа')
    def create_order(self, ingredients):
        payload = {"ingredients": ingredients}
        response = requests.post(f'{UrlKey.BASE_URL}{UrlKey.ORDERS_URL}', json=payload)
        return response.status_code, response


    @allure.step('Создание заказа без ингридиентов')
    def create_order_not_ingrit(self):
        response = requests.post(f'{UrlKey.BASE_URL}{UrlKey.ORDERS_URL}', json={})
        return response.status_code, response.json()


    @allure.step('Получение списка ингредиентов')
    def getting_ingrit_list(self):
        ingrit_list = []
        response = requests.get(f'{UrlKey.BASE_URL}{UrlKey.INGRIT_URL}')
        ingrit = response.json()
        ingrit_id = [item["_id"] for item in ingrit["data"]]
        ingrit_list.extend(ingrit_id)
        return ingrit_list


    @allure.step('Получение списка заказов конкретного пользователя')
    def getting_order_list(self, token):
        headers = {"Authorization": token}
        response = requests.get(f'{UrlKey.BASE_URL}{UrlKey.ORDERS_URL}', headers=headers)
        return response.status_code, response.json()


    @allure.step('Получение списка всех заказов без авторизации')
    def getting_all_order_list(self):
        response = requests.get(f'{UrlKey.BASE_URL}{UrlKey.ALL_ORDERS_URL}')
        return response.status_code, response.json()