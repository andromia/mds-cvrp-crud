from . import common
from app import create_app, db
from app import __version__

from config import Config

import tempfile
import logging
import pytest
import json

from . import common


ENDPOINT: str = f"{common.BASE_URL}/routes"
ROUTES = [{
    "demand_id": "",
    "depot_id": "",
    "vehicle_id": "",
    "stop_number": "",
    "unit": "",
    "user_id": ""
}]


def test_user(client):
    logging.debug(f"input_data: {common.TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, json={"routes": ROUTES})
    output = json.loads(response.data)

    assert output
