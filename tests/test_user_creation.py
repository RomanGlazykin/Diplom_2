import requests
from faker import Faker
import time
import random

def test_successful_user_creation(base_url, delete_user):
    email = f"test_{int(time.time())}_{random.randint(1000, 9999)}@{Faker().domain_name()}"
    url = f'{base_url}auth/register'
    data = {
        'email': email,
        'password': 'password',
        'name': 'pypypy'
    }
    response = requests.post(url, json=data)

    assert response.status_code == 200
    assert response.json()['success'] is True
    assert response.json()['user']['email'] == email
    assert response.json()['user']['name'] == 'pypypy'
    access_token = response.json()['accessToken']

    delete_user(access_token)

def test_user_creation_without_email(base_url):
    url = f'{base_url}auth/register'
    data = {
        'password': 'password',
        'name': 'pypypy'
    }
    response = requests.post(url, json=data)

    assert response.status_code == 403
    assert response.json()['success'] is False
    assert response.json()['message'] == "Email, password and name are required fields"

def test_user_creation_already_exists(base_url, delete_user):
    fake = Faker()
    url = f'{base_url}auth/register'
    email = f"{fake.user_name()}_{int(time.time())}@example.com"
    data = {
        'email': email,
        'password': 'password',
        'name': 'pypypy'
    }
    register_response = requests.post(url, json=data)
    assert register_response.status_code == 200
    assert register_response.json()['success'] is True
    access_token = register_response.json()['accessToken']

    second_register_response = requests.post(url, json=data)
    assert second_register_response.status_code == 403
    assert second_register_response.json()['success'] is False
    assert second_register_response.json()['message'] == "User already exists"

    delete_user(access_token)