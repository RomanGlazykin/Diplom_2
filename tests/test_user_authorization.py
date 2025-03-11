import requests
from faker import Faker

def test_valid_login(base_url, registered_user, delete_user):
    login_url = f'{base_url}auth/login'
    login_data = {
        'email': registered_user['email'],
        'password': registered_user['password']
    }
    response = requests.post(login_url, json=login_data)
    assert response.status_code == 200
    assert response.json()['success'] is True
    access_token = response.json()['accessToken']

    delete_user(access_token)

def test_invalid_login(base_url):
    fake = Faker()
    login_url = f'{base_url}auth/login'
    login_data = {
        'email': fake.email(),
        'password': fake.password()
    }
    response = requests.post(login_url, json=login_data)

    assert response.status_code == 401
    assert response.json()['success'] is False
    assert response.json()['message'] == "email or password are incorrect"