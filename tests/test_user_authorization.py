import requests
from faker import Faker
from urls import LOGIN_URL
import allure
from data import EMAIL_OR_PASSWORD_ARE_INCORRECT_MESSAGE

class TestUserAuthorization:
    @allure.title("Логин под существующим пользователем")
    def test_valid_login(self, registered_user, delete_user):
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        response = requests.post(LOGIN_URL, json=login_data)
        assert response.status_code == 200
        assert response.json()['success'] is True
        access_token = response.json()['accessToken']
        delete_user(access_token)

    @allure.title("Логин с несуществующим логином и паролем")
    def test_invalid_login(self):
        fake = Faker()
        login_data = {
            'email': fake.email(),
            'password': fake.password()
        }
        response = requests.post(LOGIN_URL, json=login_data)

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert EMAIL_OR_PASSWORD_ARE_INCORRECT_MESSAGE  in response.json()['message']