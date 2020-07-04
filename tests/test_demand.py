import pytest
import logging


def test_non_json_request(client, api_base_url: str):
    demand_endpoint = api_base_url + "/demand"
    logging.info(f'Sending request to "{demand_endpoint}"')
    res = client.post(
        demand_endpoint, headers={"Content-Type": "application/xml"}, data=""
    )
    assert res.status_code == 400


# def test_invalid_json(client, api_base_url:str):
