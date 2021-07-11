import datetime
import os
import random
from random import choice
from typing import Tuple

import faker
import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from loguru import logger

from core.db import metadata
from core.models.bigbluebutton import Meeting
from core.models.users import User, UserRoleChoices
from core.settings import DATABASE_URL
from main import app
from utils.hashing import create_access_token, get_password_hash


@pytest.fixture(scope='session', autouse=True)
def database():
    logger.info('Migrations database.')
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    yield
    logger.info('Whole test run finishes.')
    os.remove('test.db')


@pytest.fixture(scope='module')
def client():
    client_ = TestClient(app)
    return client_


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


@pytest.fixture
async def test_meeting() -> Meeting:
    fake = faker.Faker()
    datetime_start = datetime.datetime.now() + datetime.timedelta(
        days=random.randint(0, 7)
    )
    meeting = await Meeting.objects.create(
        name=fake.sentence(),
        datetime_start=datetime_start,
        datetime_end=datetime_start + datetime.timedelta(minutes=45)
    )
    return meeting


@pytest.fixture
def auth_headers(test_user) -> dict:
    password, user = test_user
    headers = {}
    token = create_access_token(data={
        'username': user.username,
        'password': password
    })
    headers['Authorization'] = f'Bearer {token}'
    return headers
