from . import common
from app import create_app, db
from app import __version__

from config import Config

import tempfile
import logging
import pytest
import json


ENDPOINT: str = f"/api/{__version__}/user"
TEST_USER: dict = {
    "username": "test",
    "password": "password"
}


def test_user(client):
    logging.debug(f"input_data: {TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, json={"user": TEST_USER})
    output = json.loads(response.data)

    assert output

    logging.debug(f"username: {TEST_USER['username']}")

    response = client.get(f"{ENDPOINT}/{TEST_USER['username']}")
    output = json.loads(response.data)

    assert output["username"] == TEST_USER["username"]