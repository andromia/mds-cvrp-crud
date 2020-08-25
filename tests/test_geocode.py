from . import common

from config import Config

import logging
import pytest
import json

from . import common


ENDPOINT: str = f"{common.BASE_URL}/geocodes"
HEADERS = dict(common.AUTH_HEADER, **{"Content-Type": "application/json"})
GEOCODES = [
    {"zipcode": "", "country": "", "latitude": "", "longitude": "", "user_id": ""}
]


def test_geocode_endpoint(client):
    logging.debug(f"input_data: {common.TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, headers=HEADERS, json={"geocodes": GEOCODES})
    output = json.loads(response.data)

    assert output
