import requests
import pytest
from faker import Faker
import time
import random
from urls import INGREDIENTS_URL, REGISTER_URL, LOGIN_URL, USER_URL

@pytest.fixture
def registered_user():
    fake = Faker()
    email = f"{fake.user_name()}_{int(time.time())}@example.com"
    data = {
        'email': email,
        'password': 'password',
        'name': 'pypypy'
    }
    response = requests.post(REGISTER_URL, json=data)
    return {
        'email': email,
        'password': 'password'
    }

@pytest.fixture
def login_user():
    def _login_user(email, password):
        login_data = {
            'email': email,
            'password': password
        }
        response = requests.post(LOGIN_URL, json=login_data)
        access_token = response.json()['accessToken']
        return access_token
    return _login_user

@pytest.fixture
def second_registered_user():
    fake = Faker()
    email = f"test_{int(time.time())}_{random.randint(1000, 9999)}@{fake.domain_name()}"
    password = "password"
    name = fake.name()
    data = {
        'email': email,
        'password': password,
        'name': name
    }
    response = requests.post(REGISTER_URL, json=data)
    access_token = response.json()['accessToken']
    return {
        'email': email,
        'password': password,
        'access_token': access_token
    }


@pytest.fixture
def delete_user(request):
    access_token = None

    def fin():
        if access_token:
            headers = {'Authorization': f'{access_token}'}
            try:
                delete_response = requests.delete(USER_URL, headers=headers)
                delete_response.raise_for_status()
            except requests.exceptions.RequestException:
                pass

    request.addfinalizer(fin)

    def _delete_user(token):
        nonlocal access_token
        access_token = token
    return _delete_user

@pytest.fixture
def available_ingredients():
    response = requests.get(INGREDIENTS_URL)
    response.raise_for_status()
    ingredients = response.json()['data']
    ingredient_ids = [ingredient['_id'] for ingredient in ingredients]
    return ingredient_ids