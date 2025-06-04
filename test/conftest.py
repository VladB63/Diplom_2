import pytest
import requests
from data import UrlKey, CreateUsers

@pytest.fixture(scope="function")
def create_new_user_and_delete():
    payload = {
        'email': CreateUsers.EMAIL,
        'password': CreateUsers.PASSWORD,
        'name': CreateUsers.NAME
    }

    response = requests.post(f'{UrlKey.BASE_URL}{UrlKey.REG_URL}', data=payload)
    response_body = response.json()
    yield payload, response_body
    access_token = response_body['accessToken']
    requests.delete(f'{UrlKey.BASE_URL}{UrlKey.CHANGE_URL}', headers={'Authorization': access_token})
