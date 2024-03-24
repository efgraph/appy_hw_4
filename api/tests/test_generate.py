import json

from http import HTTPStatus


def test_generate_image(test_client, tokens):
    response = test_client.post('/api/v1/generate_image',
                                params={'prompt': 'A beautiful landscape with a river and mountains'},
                                headers={'token': tokens.access_token})
    res = json.loads(response.content)
    assert response.status_code == HTTPStatus.OK
    assert res['prompt'] == 'A beautiful landscape with a river and mountains'
    assert len(res['imgs']) > 0
