import requests
import pytest
from faker import Faker
import time

@pytest.fixture(scope='session')
def base_url():
    return 'https://stellarburgers.nomoreparties.site/api/'

@pytest.fixture
def registered_user(base_url):
    fake = Faker()
    url = f'{base_url}auth/register'
    email = f"{fake.user_name()}_{int(time.time())}@example.com"
    data = {
        'email': email,
        'password': 'password',
        'name': 'pypypy'
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json()['success'] is True

    return {
        'email': email,
        'password': 'password'
    }

@pytest.fixture
def login_user(base_url):
    def _login_user(email, password):
        login_url = f'{base_url}auth/login'
        login_data = {
            'email': email,
            'password': password
        }
        response = requests.post(login_url, json=login_data)
        assert response.status_code == 200
        assert response.json()['success'] is True
        access_token = response.json()['accessToken']
        return access_token
    return _login_user


@pytest.fixture
def delete_user(base_url):
    def _delete_user(access_token):
        delete_url = f'{base_url}auth/user'
        headers = {'Authorization': f'{access_token}'}
        delete_response = requests.delete(delete_url, headers=headers)
        assert delete_response.status_code == 202
    return _delete_user

@pytest.fixture
def available_ingredients(base_url):
    url = f'{base_url}ingredients'  # Исправил URL
    response = requests.get(url)
    response.raise_for_status()
    ingredients = response.json()['data']
    ingredient_ids = [ingredient['_id'] for ingredient in ingredients]
    return ingredient_ids