from . import common

from config import Config

import logging
import pytest
import json

from . import common


ENDPOINT: str = f"{common.BASE_URL}/geocodes"
HEADERS = dict(common.AUTH_HEADER, **{"Content-Type": "application/json"})
GEOCODES = [{"zipcode": "", "country": "", "latitude": 1.0, "longitude": 1.0}] * 4


def test_geocode_endpoint(client):
    logging.debug(f"input_data: {common.TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(
        ENDPOINT, headers=HEADERS, json={"geocodes": GEOCODES, "stack_id": 1}
    )
    output = response.json

    assert output
