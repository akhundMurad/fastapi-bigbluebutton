from typing import Tuple

import faker

from random import choice

import pytest

from core.models.users import User, UserRoleChoices
from utils.hashing import get_password_hash


@pytest.fixture
async def test_user() -> Tuple[str, User]:
    fake = faker.Faker()
    password = fake.password()
    hashed_password = get_password_hash(password)
    user = await User.objects.create(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        password=hashed_password,
        role=choice(UserRoleChoices.values())
    )
    return password, user


def test_access_token_creating(client, test_user):
    password, test_user = test_user
    data = {
        'username': test_user.username,
        'password': password
    }

    response = client.post('/users/token/', data)

    assert response.status_code == 201
