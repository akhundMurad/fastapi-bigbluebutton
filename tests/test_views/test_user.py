import json

from db.models.users import UserRoleChoices


def test_post_user_return_201(client):
    data = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'role': UserRoleChoices.MODERATOR.value,
        'raw_password1': 'raw_password',
        'raw_password2': 'raw_password'
    }

    response = client.post('/users/register/', json=data)

    assert response.status_code == 201


def test_post_user_return_data(client):
    data = {
        'username': 'username1',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'role': UserRoleChoices.MODERATOR.value,
        'raw_password1': 'raw_password',
        'raw_password2': 'raw_password'
    }

    response = client.post('/users/register/', json=data)
    response_data = json.loads(response.content)

    assert response.status_code == 201
    assert 'id' in response_data.keys()
    del response_data['id']
    del data['raw_password1']
    del data['raw_password2']
    assert len(response_data) == len(data)
    assert all([a == b for a, b in zip(response_data, data)])
