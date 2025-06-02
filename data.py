import random

class UrlKey:
    BASE_URL = 'https://stellarburgers.nomoreparties.site/api/'
    REG_URL = 'auth/register'
    AUTH_URL = 'auth/login'
    CHANGE_URL = 'auth/user'
    INGRIT_URL = 'ingredients'
    ORDERS_URL = 'orders'
    ALL_ORDERS_URL = 'orders/all'
    LOG_OUT_URL = 'auth/logout'


class CreateUsers:

    EMAIL = f"CosmoBun{random.randint(10, 1000)}@ya.ru"
    PASSWORD = str(random.randint(10, 100))
    NAME = "Анатолий"