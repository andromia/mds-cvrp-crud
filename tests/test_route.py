import logging
import pytest
import json

from . import common

from config import Config


ENDPOINT: str = f"{common.BASE_URL}/routes"
HEADERS = dict(common.AUTH_HEADER, **{"Content-Type": "application/json"})
ROUTES = [
    {"demand_id": "", "depot_id": "", "vehicle_id": "", "stop_number": "", "unit": ""}
] * 4


def test_route_endpoint(client):
    logging.debug(f"input_data: {common.TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(
        ENDPOINT, headers=HEADERS, json={"routes": ROUTES, "stack_id": 1}
    )
    output = json.loads(response.data)

    assert output
