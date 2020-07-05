import pytest
import logging
import json

# from flask import FlaskClient
from werkzeug.wrappers import Response


class TestDemand:
    @pytest.fixture(autouse=True)
    def set_demand_endpoint(self, api_base_url):
        self.demand_endpoint: str = api_base_url + "/demand"
        logging.debug(f'Demand Endpoint "{self.demand_endpoint}"')

    @pytest.fixture(scope="class")
    def sample_demands(self):
        """Return rows of sample demands from csv file"""
        from csv import DictReader

        # Loading data from sample csv
        with open("tests/vrp_testing_data.csv") as sample_demand_file:
            sample_demand_rows = list(DictReader(sample_demand_file))

        NUM_CLUSTERS = 10

        # Cleaning individual objects in-place
        for demand in sample_demand_rows:
            demand.pop("zipcode")
            demand["latitude"] = float(demand["latitude"])
            demand["longitude"] = float(demand["longitude"])
            demand["quantity"] = float(demand.pop("weight")) / 10
            demand["unit"] = "kilograms"
            demand["cluster_id"] = int(demand.pop("pallets")) % NUM_CLUSTERS

        return sample_demand_rows

    def test_non_json_request(self, client):
        """Test with content types other than 'application/json'"""

        logging.info("Testing with content-types other than JSON")
        res: Response = client.post(
            self.demand_endpoint, headers={"Content-Type": "application/xml"}, data=""
        )
        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")
        assert res.status_code == 400
        assert res.headers["Content-Type"] == "application/json"
        assert (
            res.json["message"] == "Incorrect request format! Request data must be JSON"
        )

    def test_invalid_json(self, client):
        """Test with invalid JSON in request"""
        logging.info("Testing with invalid JSON")
        logging.debug(f'Sending request to "{self.demand_endpoint}"')
        res: Response = client.post(
            self.demand_endpoint,
            headers={"Content-Type": "application/json"},
            data='{"dfd',
        )
        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")
        assert res.status_code == 400
        assert res.headers["Content-Type"] == "application/json"
        assert res.json["message"] == "Invalid JSON received! Request data must be JSON"

    def test_empty_demand(self, client):
        """Test by sending empty demand array"""
        logging.info("Testing with empty demands array")
        res: Response = client.post(
            self.demand_endpoint,
            headers={"Content-Type": "application/json"},
            json={"demands": []},
        )
        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")
        assert res.status_code == 400
        assert res.headers["Content-Type"] == "application/json"

        error_message = res.json["message"]
        assert error_message == "'demands' is empty"

    @pytest.mark.parametrize(
        "param", ["latitude", "longitude", "cluster_id", "unit_name", "quantity"]
    )
    def test_invalid_demand(self, client, param):
        """Test with invalid parameters in demand"""
        pass

    def test_single_insert(self, sample_demands: list):
        """Test with single demand"""
        pass

    def test_batch_insert(self, sample_demands: list):
        """Test with multiple demands"""
        pass
