import allure
import pytest
from data import CreateUsers
from methods.users_methods import UsersMethods

class TestUsers:

    @allure.title('Проверка успешного создания пользователя')
    def test_create_users(self):
        usm = UsersMethods()
        status_code, response = usm.create_users()
        assert status_code == 200 and response
        usm.del_user()

    @allure.title('Проверка создания дубля пользователя')
    def test_create_double_users(self):
        usm = UsersMethods()
        usm.create_users()
        usm.create_users()
        status_code, response = usm.create_users()
        assert status_code == 403 and response == {"success": False, "message": "User already exists"}

    @allure.title('Проверка создания пользователя с не полными данными')
    @pytest.mark.parametrize(
        "payload", [
            {'email': CreateUsers.EMAIL, 'password': CreateUsers.PASSWORD},
            {'password': CreateUsers.PASSWORD, 'name': CreateUsers.NAME}
        ]
    )
    def test_create_user_fail(self, payload):
        usm = UsersMethods()
        status_code, response = usm.create_user_fail(payload)
        assert status_code == 403 and response == {"success": False,
                                                   "message": "Email, password and name are required fields"}


    @allure.title('Проверка авторизации пользователя')
    def test_auth_user_passed(self):
        usm = UsersMethods()
        usm.create_users()
        status_code, response = usm.log_user()
        assert status_code == 200 and response
        usm.del_user()


    @allure.title('Проверка авторизации под не существующим пользователем')
    @pytest.mark.parametrize(
        "payload", [
            {'email': CreateUsers.PASSWORD, 'password': CreateUsers.PASSWORD}
        ]
    )
    def test_auth_user_fail(self, payload):
        usm = UsersMethods()
        status_code, response = usm.log_user_failed(payload)
        assert status_code == 401 and response == {"success": False,
                                                   "message": "email or password are incorrect"}


    @allure.title('Проверка возможности изменения пользователя после авторизации')
    def test_change_user(self):
        usm = UsersMethods()
        usm.create_users()
        usm.log_user()
        status_code, response = usm.change_user()
        assert status_code == 200 and response
        usm.del_user()


    @allure.title('Проверка возможности изменения пользователя без авторизации')
    def test_change_user_fail(self):
        usm = UsersMethods()
        status_code, response = usm.change_user_fail()
        assert status_code == 401 and response == {"success": False,
                                                   "message": "You should be authorised"}

