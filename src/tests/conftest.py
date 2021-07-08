import os
import pytest
import sqlalchemy

from loguru import logger

from fastapi.testclient import TestClient

from core.db import metadata
from core.settings import DATABASE_URL
from main import app


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
