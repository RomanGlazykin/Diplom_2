import requests
from faker import Faker
import time
import random
from urls import REGISTER_URL
import allure
from data import EMAIL_PASSWORD_AND_NAME_ARE_REQUIRED_FIELDS_MESSAGE, USER_ALREADY_EXISTS_MESSAGE

class TestUserCreation:
    @allure.title("создать уникального пользователя")
    def test_successful_user_creation(self, delete_user):
        email = f"test_{int(time.time())}_{random.randint(1000, 9999)}@{Faker().domain_name()}"
        data = {
            'email': email,
            'password': 'password',
            'name': 'pypypy'
        }
        response = requests.post(REGISTER_URL, json=data)
        assert response.status_code == 200
        assert response.json()['success'] is True
        access_token = response.json()['accessToken']
        delete_user(access_token)

    @allure.title("создать пользователя и не заполнить одно из обязательных полей")
    def test_user_creation_without_email(self):
        data = {
            'password': 'password',
            'name': 'pypypy'
        }
        response = requests.post(REGISTER_URL, json=data)

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert EMAIL_PASSWORD_AND_NAME_ARE_REQUIRED_FIELDS_MESSAGE in response.json()['message']

    @allure.title("создать пользователя, который уже зарегистрирован")
    def test_user_creation_already_exists(self, delete_user):
        fake = Faker()
        email = f"{fake.user_name()}_{int(time.time())}@example.com"
        data = {
            'email': email,
            'password': 'password',
            'name': 'pypypy'
        }
        register_response = requests.post(REGISTER_URL, json=data)
        access_token = register_response.json()['accessToken']

        second_register_response = requests.post(REGISTER_URL, json=data)
        assert second_register_response.status_code == 403
        assert second_register_response.json()['success'] is False
        assert USER_ALREADY_EXISTS_MESSAGE in second_register_response.json()['message']
        delete_user(access_token)
