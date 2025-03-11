import requests

def test_create_order_with_authorization(base_url, registered_user, login_user, delete_user, available_ingredients):
    email = registered_user['email']
    password = registered_user['password']
    access_token = login_user(email, password)

    url = f'{base_url}orders'
    headers = {'Authorization': f'{access_token}'}
    ingredients = available_ingredients[:2]
    data = {"ingredients": ingredients}
    response = requests.post(url, headers=headers, json=data)

    response_body = response.json()
    assert response.status_code == 200
    assert response.json()['success'] is True
    assert 'order' in response_body
    assert 'number' in response_body['order']

    delete_user(access_token)

def test_create_order_without_authorization(base_url,available_ingredients):
    url = f'{base_url}orders'
    ingredients = available_ingredients[:2]
    data = {"ingredients": ingredients}
    response = requests.post(url, json=data)

    assert response.status_code == 401 #баг-репорт
    assert response.json()['success'] is False
    assert response.json()['message'] == "You should be authorised"

def test_create_order_without_ingredients(base_url, registered_user, login_user, delete_user):
    email = registered_user['email']
    password = registered_user['password']
    access_token = login_user(email, password)

    url = f'{base_url}orders'
    headers = {'Authorization': f'{access_token}'}
    data = {"ingredients": []}
    response = requests.post(url, headers=headers, json=data)

    assert response.status_code == 400
    response_body = response.json()
    assert response_body['success'] is False
    assert response_body['message'] == "Ingredient ids must be provided"


def test_create_order_with_invalid_ingredients(base_url, registered_user, login_user, delete_user):
    email = registered_user['email']
    password = registered_user['password']
    access_token = login_user(email, password)

    url = f'{base_url}orders'
    headers = {'Authorization': f'{access_token}'}
    invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
    data = {"ingredients": invalid_ingredients}
    response = requests.post(url, headers=headers, json=data)

    assert response.status_code == 500