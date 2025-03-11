import requests
from faker import Faker
import time
import random

def test_changing_login_user(base_url, registered_user, login_user, delete_user):
    email = registered_user['email']
    password = registered_user['password']
    access_token = login_user(email, password)

    changing_url = f'{base_url}auth/user'
    headers = {'Authorization': f'{access_token}'}
    changing_data = {
        'email': 'pupupu1@gmail.com',
        'name': 'ререре'
    }
    response = requests.patch(changing_url, headers=headers, json=changing_data)
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert response.json()['user']['email'] == 'pupupu1@gmail.com'
    assert response.json()['user']['name'] == 'ререре'

    delete_user(access_token)

def test_changing_use_mail(base_url, registered_user, login_user, delete_user):
    user1_data = registered_user
    fake = Faker()
    user2_email = f"test_{int(time.time())}_{random.randint(1000, 9999)}@{fake.domain_name()}"
    user2_password = "password"
    user2_name = fake.name()
    user2_data = {
        'email': user2_email,
        'password': user2_password,
        'name': user2_name
    }

    register_url = f'{base_url}auth/register'
    response = requests.post(register_url, json=user2_data)
    assert response.status_code == 200
    access_token_user2 = response.json()['accessToken']

    access_token_user1 = login_user(user1_data['email'], user1_data['password'])

    changing_url = f'{base_url}auth/user'
    headers = {'Authorization': f'{access_token_user1}'}
    changing_data = {
        'email': user2_email
    }
    response = requests.patch(changing_url, headers=headers, json=changing_data)

    assert response.status_code == 403
    assert response.json()['success'] is False
    assert "User with such email already exists" in response.json()['message']

    delete_user(access_token_user1)
    delete_user(access_token_user2)

def test_changing_logout_user(base_url):
    fake = Faker()
    changing_url = f'{base_url}auth/user'
    changing_data = {
        'email': fake.email(),
        'name': fake.name()
    }
    response = requests.patch(changing_url, json=changing_data)
    assert response.status_code == 401
    assert response.json()['success'] is False
    assert response.json()['message'] == "You should be authorised"