from . import common
from config import Config

import logging
import pytest
import json


ENDPOINT: str = f"{common.BASE_URL}/geocode"
GEOCODES: list = [{"zipcode": "", "country": "", "latitude": 1.0, "longitude": 1.0}] * 4


def test_geocode_endpoint(client, auth_header: dict):
    input_data: dict = {"geocodes": GEOCODES, "stack_id": 1}
    logging.debug(f"Input data: {input_data}")
    logging.debug(f"Endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, headers=auth_header, json=input_data)
    output = response.json

    assert output
