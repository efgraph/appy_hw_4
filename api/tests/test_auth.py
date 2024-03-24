import json
from http import HTTPStatus

from model.models import SignUpUser, Tokens


def test_signup(test_client):
    response = test_client.post('/api/v1/signup', json={
        'username': 'username', 'password': '12345', 'email': 'username@mail.ru'
    })
    if response.status_code == HTTPStatus.BAD_REQUEST:
        res = json.loads(response.content.decode('utf-8'))
        assert res['detail'] == 'Username already registered'
    else:
        signup_user = SignUpUser.model_validate_json(response.content)
        assert response.status_code == HTTPStatus.OK
        assert signup_user.username
        assert signup_user.email


def test_login(test_client):
    response = test_client.post('/api/v1/login',
                                json={'username': 'username', 'password': '12345'})
    tokens = Tokens.model_validate_json(response.content)
    assert response.status_code == HTTPStatus.OK
    assert tokens.access_token
    assert tokens.refresh_token


def test_token_update(test_client, tokens):
    response = test_client.post('/api/v1/update/token', headers={'token': tokens.refresh_token})
    tokens = Tokens.model_validate_json(response.content)
    assert response.status_code == HTTPStatus.OK
    assert tokens.access_token
    assert tokens.refresh_token


def test_logout(test_client, tokens):
    response = test_client.post('/api/v1/logout', headers={'token': tokens.access_token})
    assert response.status_code == HTTPStatus.OK
    assert json.loads(response.content.decode('utf-8')) == {'msg': 'Logged out'}
    response = test_client.post('/logout', headers={'token': tokens.access_token})
    assert response.status_code == HTTPStatus.NOT_FOUND
