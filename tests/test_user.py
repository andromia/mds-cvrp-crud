import logging
import pytest
import json

from . import common

from config import Config


ENDPOINT: str = f"{common.BASE_URL}/user"
TEST_USER: dict = {"username": "test", "password": "password"}


def test_user_endpoint(client):
    logging.debug(f"input_data: {TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, json={"user": TEST_USER})
    output = json.loads(response.data)

    assert output

    logging.debug(f"username: {TEST_USER['username']}")

    response = client.get(f"{ENDPOINT}/{TEST_USER['username']}")
    user = json.loads(response.data)["user"]

    assert user["username"] == TEST_USER["username"]
