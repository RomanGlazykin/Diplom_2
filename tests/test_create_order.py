import requests
from urls import ORDERS_URL
import allure
from data import YOU_SHOULD_BE_AUTHORIZED_MESSAGE, INGREDIENT_IDS_MUST_BE_PROVIDED_MESSAGE


class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_authorization(self, registered_user, login_user, delete_user, available_ingredients):
        email = registered_user['email']
        password = registered_user['password']
        access_token = login_user(email, password)

        headers = {'Authorization': f'{access_token}'}
        ingredients = available_ingredients[:2]
        data = {"ingredients": ingredients}
        response = requests.post(ORDERS_URL, headers=headers, json=data)

        response_body = response.json()
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response_body
        assert 'number' in response_body['order']
        delete_user(access_token)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self, available_ingredients):
        ingredients = available_ingredients[:2]
        data = {"ingredients": ingredients}
        response = requests.post(ORDERS_URL, json=data)

        assert response.status_code == 401  # баг-репорт
        assert response.json()['success'] is False
        assert YOU_SHOULD_BE_AUTHORIZED_MESSAGE in response.json()['message']

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user, login_user, delete_user):
        email = registered_user['email']
        password = registered_user['password']
        access_token = login_user(email, password)

        headers = {'Authorization': f'{access_token}'}
        data = {"ingredients": []}
        response = requests.post(ORDERS_URL, headers=headers, json=data)

        assert response.status_code == 400
        response_body = response.json()
        assert response_body['success'] is False
        assert INGREDIENT_IDS_MUST_BE_PROVIDED_MESSAGE in response_body['message']
        delete_user(access_token)

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self, registered_user, login_user, delete_user):
        email = registered_user['email']
        password = registered_user['password']
        access_token = login_user(email, password)

        headers = {'Authorization': f'{access_token}'}
        invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
        data = {"ingredients": invalid_ingredients}
        response = requests.post(ORDERS_URL, headers=headers, json=data)

        assert response.status_code == 500
        delete_user(access_token)
