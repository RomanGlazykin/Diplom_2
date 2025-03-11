import requests

def test_get_orders_with_authorization(base_url, registered_user, login_user):
    email = registered_user['email']
    password = registered_user['password']
    access_token = login_user(email, password)

    url = f'{base_url}orders'
    headers = {'Authorization': f'{access_token}'}
    response = requests.get(url, headers=headers)

    assert response.status_code == 200
    assert response.json()['success'] is True
    assert 'orders' in response.json()


def test_get_orders_without_authorization(base_url):
    url = f'{base_url}orders'
    response = requests.get(url)

    assert response.status_code == 401
    assert response.json()['success'] is False
    assert response.json()['message'] == "You should be authorised"