def test_access_token_creating(client, test_user):
    password, test_user = test_user
    data = {
        'username': test_user.username,
        'password': password
    }

    response = client.post('/users/token/', data)

    assert response.status_code == 201
