import allure
import pytest
from data import CreateUsers
from methods.users_methods import UsersMethods
from test.conftest import create_new_user_and_delete

class TestUsers:


    @allure.title('Проверка создания пользователя с не полными данными')
    @pytest.mark.parametrize(
        "payload", [
            {'email': CreateUsers.EMAIL, 'password': CreateUsers.PASSWORD},
            {'password': CreateUsers.PASSWORD, 'name': CreateUsers.NAME}
        ]
    )
    def test_create_user_fail(self, payload):
        usm = UsersMethods()
        status_code, response = usm.create_users(payload)
        assert status_code == 403 and response == {"success": False,
                                                   "message": "Email, password and name are required fields"}

    @allure.title('Проверка авторизации под не существующим пользователем')
    def test_auth_user_fail(self):
        usm = UsersMethods()
        status_code, response = usm.log_user()
        assert status_code == 401 and response == {"success": False,
                                                   "message": "email or password are incorrect"}


    @allure.title('Проверка авторизации пользователя')
    def test_auth_user_passed(self, create_new_user_and_delete):
        payload, response_body = create_new_user_and_delete
        usm = UsersMethods()
        status_code, response = usm.log_user()
        assert status_code == 200 and response['accessToken']



    @allure.title('Проверка возможности изменения пользователя после авторизации')
    def test_change_user(self, create_new_user_and_delete):
        payload, response = create_new_user_and_delete
        usm = UsersMethods()
        usm.log_user()
        status_code, response = usm.change_user()
        assert status_code == 200 and response['user']


    @allure.title('Проверка возможности изменения пользователя без авторизации')
    def test_change_user_fail(self):
        usm = UsersMethods()
        status_code, response = usm.change_user_fail()
        assert status_code == 401 and response == {"success": False,
                                                   "message": "You should be authorised"}


        @allure.title('Проверка успешного создания пользователя')
        @pytest.mark.parametrize(
            "payload", [
                {'email': CreateUsers.EMAIL, 'password': CreateUsers.PASSWORD, 'name': CreateUsers.NAME}
            ]
        )
        def test_create_users(self, payload):
            usm = UsersMethods()
            status_code, response = usm.create_users(payload)
            assert status_code == 200 and response['user']
            usm.del_user()


        @allure.title('Проверка создания дубля пользователя')
        @pytest.mark.parametrize(
            "payload", [
                {'email': CreateUsers.EMAIL, 'password': CreateUsers.PASSWORD, 'name': CreateUsers.NAME}
            ]
        )
        def test_create_double_users(self, payload):
            usm = UsersMethods()
            usm.create_users(payload)
            usm.create_users(payload)
            status_code, response = usm.create_users(payload)
            assert status_code == 403 and response == {"success": False, "message": "User already exists"}


