import allure
import pytest
from methods.users_methods import UsersMethods
from methods.order_methods import OrderMethods
from test.conftest import create_new_user_and_delete

class TestOrder:

    @allure.title('Проверка успешного создания заказа c авторизацией и ингредиентами')
    def test_create_order_in_auth_with_ingrit(self, create_new_user_and_delete):
        usm = UsersMethods()
        om = OrderMethods()
        payload, response = create_new_user_and_delete
        usm.log_user()
        ingrit = om.getting_ingrit_list()
        order_ingrit = [ingrit[0], ingrit[1]]
        status_code, response = om.create_order(order_ingrit)
        assert status_code == 200 and response['order']



    @allure.title('Проверка успешного создания заказа c авторизацией и без ингредиентов')
    def test_create_order_in_auth_not_ingrit(self, create_new_user_and_delete):
        usm = UsersMethods()
        om = OrderMethods()
        payload, response = create_new_user_and_delete
        usm.log_user()
        status_code, response = om.create_order_not_ingrit()
        assert status_code == 400 and response == {"success": False,
                                                  "message": "Ingredient ids must be provided"}



    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_not_auth(self):
        om = OrderMethods()
        ingrit = om.getting_ingrit_list()
        order_ingrit = [ingrit[0], ingrit[1]]
        status_code, response = om.create_order(order_ingrit)
        assert status_code == 200 and response['order']


    @allure.title('Проверка создания заказа с неверным хешем ингредиентов')
    @pytest.mark.parametrize(
        "ingrit", [
            ("61c0c5a71d1f82001bdaaa6d", "4wrwrewr"),
            ("45645456456", "61c0c5a71d1f82001bdaaa6f")
        ]
    )
    def test_create_order_in_correct_ingrit(self, ingrit, create_new_user_and_delete):
        usm = UsersMethods()
        om = OrderMethods()
        payload, response = create_new_user_and_delete
        usm.log_user()
        status_code, response = om.create_order_500(ingrit)
        assert status_code == 500 and ['Internal Server Error']
        usm.del_user()


    @allure.title('Проверка получения заказов авторизованный пользователь')
    def test_giv_order_list_with_auth(self, create_new_user_and_delete):
        usm = UsersMethods()
        om = OrderMethods()
        payload, response = create_new_user_and_delete
        _, response = usm.log_user()
        token = response.get('accessToken')
        ingrit = om.getting_ingrit_list()
        order_ingrit = [ingrit[0], ingrit[1]]
        om.create_order(order_ingrit)
        om.create_order(order_ingrit)
        status_code, response = om.getting_order_list(token)
        assert status_code == 200 and ['orders']
        usm.del_user()


    @allure.title('Проверка получения заказов не авторизованный пользователь')
    def test_giv_order_list_not_auth(self):
        om = OrderMethods()
        status_code, response = om.getting_order_list_not_auth()
        assert status_code == 401 and response == {"success": False,
                                                   "message": "You should be authorised"}


    @allure.title('Проверка получения все заказов')
    def test_giv_all_order_list(self):
        om = OrderMethods()
        status_code, response = om.getting_all_order_list()
        assert status_code == 200 and response['orders']


