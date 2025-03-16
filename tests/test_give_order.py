import requests
from urls import ORDERS_URL
import allure
from data import YOU_SHOULD_BE_AUTHORIZED_MESSAGE

class TestGiveOrder:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_authorization(self, registered_user, login_user, delete_user):
        email = registered_user['email']
        password = registered_user['password']
        access_token = login_user(email, password)

        headers = {'Authorization': f'{access_token}'}
        response = requests.get(ORDERS_URL, headers=headers)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'orders' in response.json()
        delete_user(access_token)

    @allure.title("Получение заказов не авторизованного пользователя")
    def test_get_orders_without_authorization(self):
        response = requests.get(ORDERS_URL)

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert YOU_SHOULD_BE_AUTHORIZED_MESSAGE in response.json()['message']