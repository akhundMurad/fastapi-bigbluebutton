import asyncio
import datetime
import random
from random import choice
from typing import Tuple

import faker
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db import models, choices
from src.core.settings import Settings
from src.main import get_app
from src.services.users.user import create_access_token, get_password_hash


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return get_app()


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session', autouse=True)
def session(settings) -> AsyncSession:
    logger.info('Migrations database.')
    engine = create_async_engine(str(settings.database_dsn), future=True, echo=True)
    session_maker = sessionmaker(
        engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        class_=AsyncSession,
    )
    yield session_maker()
    logger.info('Whole test run finishes.')


@pytest.fixture(scope='module')
def client(app):
    client_ = TestClient(app)
    return client_


@pytest.fixture
async def test_user(session) -> Tuple[str, models.User]:
    fake = faker.Faker()
    password = fake.password()
    hashed_password = get_password_hash(password)
    user = models.User(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        password=hashed_password,
        role=choice(choices.UserRoleChoices.values())
    )
    await session.add(user)
    await session.commit()
    await session.refresh(user)
    return password, user


@pytest.fixture
async def test_meeting(session) -> models.Meeting:
    fake = faker.Faker()
    datetime_start = datetime.datetime.now() + datetime.timedelta(
        days=random.randint(0, 7)
    )
    meeting = models.Meeting(
        name=fake.sentence(),
        datetime_start=datetime_start,
        datetime_end=datetime_start + datetime.timedelta(minutes=45)
    )
    await session.add(meeting)
    await session.commit()
    await session.refresh(meeting)
    return meeting


@pytest.fixture
def auth_headers(test_user) -> dict:
    password, user = test_user
    headers = {}
    token = create_access_token(data={'sub': user.username})
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


@pytest.fixture
async def test_schedule(test_user, session) -> Tuple[models.User, models.Schedule]:
    _, user = test_user

    schedule = models.Schedule()
    schedule.attendee_list.append(user)
    await session.add(schedule)
    await session.commit()
    await session.refresh(schedule)
    return user, schedule


@pytest.fixture
async def test_schedule_cell(test_schedule) -> Tuple[models.User, models.ScheduleCell]:
    user, test_schedule = test_schedule
    datetime_start = datetime.datetime.now() + datetime.timedelta(
        days=random.randint(0, 7)
    )
    cell = models.ScheduleCell(
        datetime_start=datetime_start,
        datetime_end=datetime_start + datetime.timedelta(minutes=45),
        schedule=test_schedule
    )

    await session.add(cell)
    await session.commit()
    await session.refresh(cell)

    return user, cell
