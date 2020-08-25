import logging
import pytest
import json

from . import common

from config import Config


ENDPOINT: str = f"{common.BASE_URL}/stack"
HEADERS = dict(common.AUTH_HEADER, **{"Content-Type": "application/json"})
STACK = {"stack": {"name": ""}, "chain": [{"id": ""}, {"id": ""}]}


def test_stack_endpoint(client):
    logging.debug(f"input_data: {common.TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, headers=HEADERS, json=STACK)
    output = json.loads(response.data)

    assert output
