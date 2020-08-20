from . import common
from app import create_app
from app import __version__

from config import Config

import logging
import pytest
import json


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture
def client():
    yield create_app(TestConfig).test_client()


def test_user(client):
    pass
