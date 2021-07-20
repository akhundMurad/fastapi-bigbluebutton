import asyncio
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
from redis import init_redis_pool
from utils.hashing import create_access_token, get_password_hash


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session', autouse=True)
def database():
    logger.info('Migrations database.')
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    yield
    logger.info('Whole test run finishes.')
    os.remove('test.db')


@pytest.fixture(scope='session', autouse=True)
async def redis():
    logger.info('Creating Redis pool')
    app.state.redis = await init_redis_pool()
    yield app.state.redis
    app.state.redis.close()
    await app.state.redis.wait_closed()


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


@pytest.fixture
def meeting_end_response(mocker):
    mocked_get = mocker.patch('bigbluebutton.api.httpx.AsyncClient.get')
    response = mocker.Mock()
    response.status_code = 200
    with open('tests/data/response_end.xml', 'r') as file:
        response.text = file.read()

    mocked_get.return_value = response


@pytest.fixture
def meeting_create_response(mocker):
    mocked_get = mocker.patch('bigbluebutton.api.httpx.AsyncClient.get')
    response = mocker.Mock()
    response.status_code = 200
    with open('tests/data/response_create.xml', 'r') as file:
        response.text = file.read()

    mocked_get.return_value = response


@pytest.fixture
def meeting_get_meeting_info_response(mocker):
    mocked_get = mocker.patch('bigbluebutton.api.httpx.AsyncClient.get')
    response = mocker.Mock()
    response.status_code = 200
    with open('tests/data/response_get_meeting_info.xml', 'r') as file:
        response.text = file.read()

    mocked_get.return_value = response


@pytest.fixture
def meeting_get_meetings_response(mocker):
    mocked_get = mocker.patch('bigbluebutton.api.httpx.AsyncClient.get')
    response = mocker.Mock()
    response.status_code = 200
    with open('tests/data/response_get_meetings.xml', 'r') as file:
        response.text = file.read()

    mocked_get.return_value = response


@pytest.fixture
def meeting_is_meeting_running_response(mocker):
    mocked_get = mocker.patch('bigbluebutton.api.httpx.AsyncClient.get')
    response = mocker.Mock()
    response.status_code = 200
    with open('tests/data/response_is_meeting_running.xml', 'r') as file:
        response.text = file.read()

    mocked_get.return_value = response


@pytest.fixture
def meeting_join_response(mocker):
    mocked_get = mocker.patch('bigbluebutton.api.httpx.AsyncClient.get')
    response = mocker.Mock()
    response.status_code = 200
    with open('tests/data/response_join.xml', 'r') as file:
        response.text = file.read()

    mocked_get.return_value = response
