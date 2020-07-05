import pytest
import logging
import json

import string
import random
from csv import DictReader

from typing import List

# from flask import FlaskClient
from werkzeug.wrappers import Response


class TestDemand:
    @pytest.fixture(autouse=True)
    def set_demand_endpoint(self, api_base_url):
        """Set demand endpoint as object variable"""

        self.demand_endpoint: str = api_base_url + "/demand"
        logging.debug(f'Demand Endpoint "{self.demand_endpoint}"')

    @pytest.fixture(scope="class")
    def sample_demands(self):
        """Return rows of sample demands from csv file"""

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

    @pytest.fixture()
    def random_demand(self):
        """Return random generated demand"""

        return {
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
            "quantity": random.uniform(0, 20000),
            "cluster_id": random.randint(0, 100),
            "unit": "".join(
                random.choices(string.ascii_lowercase, k=random.randint(1, 10))
            ),
        }

    @pytest.mark.parametrize(
        "content_type",
        [
            "audio/aac",
            "application/x-abiword",
            "application/x-freearc",
            "video/x-msvideo",
            "application/vnd.amazon.ebook",
            "application/octet-stream",
            "image/bmp",
            "application/x-bzip",
            "application/x-bzip2",
            "application/x-csh",
            "text/css",
            "text/csv",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-fontobject",
            "application/epub+zip",
            "application/gzip",
            "image/gif",
            "text/html",
            "image/vnd.microsoft.icon",
            "text/calendar",
            "application/java-archive",
            "image/jpeg",
            "text/javascript, per the following specifications:",
            "audio/midi",
            "text/javascript",
            "audio/mpeg",
            "video/mpeg",
            "application/vnd.apple.installer+xml",
            "application/vnd.oasis.opendocument.presentation",
            "application/vnd.oasis.opendocument.spreadsheet",
            "application/vnd.oasis.opendocument.text",
            "audio/ogg",
            "video/ogg",
            "application/ogg",
            "audio/opus",
            "font/otf",
            "image/png",
            "application/pdf",
            "application/x-httpd-php",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/vnd.rar",
            "application/rtf",
            "application/x-sh",
            "image/svg+xml",
            "application/x-shockwave-flash",
            "application/x-tar",
            "image/tiff",
            "video/mp2t",
            "font/ttf",
            "text/plain",
            "application/vnd.visio",
            "audio/wav",
            "audio/webm",
            "video/webm",
            "image/webp",
            "font/woff",
            "font/woff2",
            "application/xhtml+xml",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/xml ",
            "application/vnd.mozilla.xul+xml",
            "application/zip",
            "video/3gpp",
            "video/3gpp2",
            "application/x-7z-compressed",
        ],
    )
    def test_non_json_request(self, client, content_type):
        """Test with content types other than 'application/json'"""

        logging.info(f"Testing with content-type : {content_type}")

        res: Response = client.post(
            self.demand_endpoint, headers={"Content-Type": content_type}, data=""
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
            data="".join(
                random.choices(
                    string.ascii_letters + "".join(["{", "}", '"', "'"]),
                    k=random.randint(1, 27),
                )
            ),
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
        "param", ["latitude", "longitude", "unit", "cluster_id", "quantity"]
    )
    def test_invalid_demand(self, client, param, random_demand):
        """Test with invalid parameters in demand"""

        demand = random_demand
        logging.debug(f"Demand : {demand}")

        invalid_choices = {
            "latitude": [
                random.uniform(-10000, -90.1),
                random.uniform(90.1, 10000),
                "".join(
                    random.choices(
                        string.ascii_letters + "".join(["{", "}", '"', "'"]),
                        k=random.randint(1, 27),
                    )
                ),
            ],
            "longitude": [
                random.uniform(-10000, -90.1),
                random.uniform(90.1, 10000),
                "".join(
                    random.choices(
                        string.ascii_letters + "".join(["{", "}", '"', "'"]),
                        k=random.randint(1, 27),
                    )
                ),
            ],
            "cluster_id": [
                random.uniform(-10000, 0),
                random.uniform(0, -10000),
                random.randint(-10000, 0),
                random.randint(0, 10000),
                "".join(
                    random.choices(
                        string.ascii_letters + "".join(["{", "}", '"', "'"]),
                        k=random.randint(1, 27),
                    )
                ),
            ],
            "unit": [
                random.uniform(-10000, 0),
                random.uniform(0, -10000),
                random.randint(-10000, 0),
                random.randint(0, 10000),
                "".join(
                    random.choices(
                        string.ascii_letters + "".join(["{", "}", '"', "'"]),
                        k=random.randint(1, 10),
                    )
                ),
            ],
            "quantity": [
                random.randint(-10000, 0),
                "".join(
                    random.choices(
                        string.ascii_letters + "".join(["{", "}", '"', "'"]),
                        k=random.randint(1, 10),
                    )
                ),
            ],
        }

        demand[param] = random.choice(invalid_choices[param])

        logging.debug(f"Invalid Demand : {demand}")

        res: Response = client.post(
            self.demand_endpoint,
            headers={"Content-Type": "application/json"},
            json={"demands": [demand]},
        )

        assert res.status_code == 400
        assert f"Invalid {param}" in res.json["message"]

    def test_single_insert(self, client, sample_demands: List[dict]):
        """Test with single demand"""

        sample_demand = random.choice(sample_demands)

        logging.debug(f"Demand : {sample_demand}")

        res: Response = client.post(
            self.demand_endpoint,
            headers={"Content-Type": "application/json"},
            json={"demands": [sample_demand]},
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 200
        assert res.headers["Content-Type"] == "application/json"
        for demand, response in zip(sample_demands, res.json):
            id = response.pop("id")
            assert isinstance(id, int)
            assert demand == response
            response["id"] = id

    def test_batch_insert(self, client, sample_demands: List[dict]):
        """Test with multiple demands"""

        logging.info("Testing with multiple demands in one request")

        res: Response = client.post(
            self.demand_endpoint,
            headers={"Content-Type": "application/json"},
            json={"demands": sample_demands},
        )

        assert res.status_code == 200
        assert len(res.json) == len(sample_demands)

        for demand, response in zip(sample_demands, res.json):
            id = response.pop("id")
            assert isinstance(id, int)
            assert demand == response
            response["id"] = id

