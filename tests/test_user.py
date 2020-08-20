from . import common
from app import create_app, db
from app import __version__

from config import Config

import tempfile
import logging
import pytest
import json


def test_user_post(client, api_base_url):
    input_data = {
        "user": {
            "username": "test",
            "password": "test"
        }
    }
    logging.debug(f"input_data: {input_data}")

    endpoint: str= api_base_url + "/user"
    logging.debug(f"endpoint: {endpoint}")

    response = client.post(endpoint, json=input_data)
    output = json.loads(response.data)

    assert output