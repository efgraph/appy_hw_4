import pytest
from fastapi.testclient import TestClient

from main import app
from model.models import Tokens


@pytest.fixture(scope='module')
def test_client():
    test_client = TestClient(app=app)
    yield test_client


@pytest.fixture(scope='module')
def tokens(test_client):
    test_client.post('/api/v1/signup', json={
        'username': 'admin', 'password': 'admin', 'email': 'admin@mail.ru'
    })
    response = test_client.post('/api/v1/login',
                                json={'username': 'admin', 'password': 'admin'})
    tokens = Tokens.model_validate_json(response.content)
    yield tokens
