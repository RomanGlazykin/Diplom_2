import requests
from faker import Faker
from urls import USER_URL, REGISTER_URL
import allure
from data import USER_WITH_SUCH_EMAIL_ALREADY_EXISTS_MESSAGE, YOU_SHOULD_BE_AUTHORIZED_MESSAGE


class TestChangingUserData:
    @allure.title("Изменение логина пользователя")
    def test_changing_login_user(self, registered_user, login_user, delete_user):
        email = registered_user['email']
        password = registered_user['password']
        access_token = login_user(email, password)

        headers = {'Authorization': f'{access_token}'}
        changing_data = {
            'email': 'pupu10101010@gmail.com',
            'name': 'ререре'
        }
        response = requests.patch(USER_URL, headers=headers, json=changing_data)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == 'pupu10101010@gmail.com'
        assert response.json()['user']['name'] == 'ререре'
        delete_user(access_token)

    @allure.title("Изменение email пользователя на уже существующий")
    def test_changing_use_mail(self, registered_user, login_user, second_registered_user, delete_user):
        user1_data = registered_user
        user2_data = second_registered_user

        access_token_user1 = login_user(user1_data['email'], user1_data['password'])
        access_token_user2 = user2_data['access_token']

        headers = {'Authorization': f'{access_token_user1}'}
        changing_data = {
            'email': user2_data['email']
        }
        response = requests.patch(USER_URL, headers=headers, json=changing_data)

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert USER_WITH_SUCH_EMAIL_ALREADY_EXISTS_MESSAGE in response.json()['message']

        delete_user(access_token_user1)
        delete_user(access_token_user2)

    @allure.title("Изменение данных неавторизованного пользователя")
    def test_changing_logout_user(self):
        fake = Faker()
        changing_data = {
            'email': fake.email(),
            'name': fake.name()
        }
        response = requests.patch(USER_URL, json=changing_data)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert YOU_SHOULD_BE_AUTHORIZED_MESSAGE in response.json()['message']