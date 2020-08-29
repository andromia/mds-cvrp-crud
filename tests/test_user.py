from . import common
from config import Config

import logging
import pytest
import json


ENDPOINT: str = f"{common.BASE_URL}/user"


def test_user_endpoint(client):
    logging.debug(f"input_data: {common.TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, json={"user": common.TEST_USER})
    output = json.loads(response.data)

    assert output

    logging.debug(f"username: {common.TEST_USER['username']}")

    response = client.get(f"{ENDPOINT}/{common.TEST_USER['username']}")
    user: dict = json.loads(response.data)["user"]

    assert user["username"] == common.TEST_USER["username"]
