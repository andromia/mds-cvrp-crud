import pytest
import logging
import json

import random
import string

from typing import List, Dict

# from flask import FlaskClient
from werkzeug.wrappers import Response


class TestDepot:
    @pytest.fixture(autouse=True)
    def set_depot_endpoint(self, api_base_url):
        """Set depot endpoint as object variable"""

        self.depot_endpoint: str = api_base_url + "/depot"
        logging.debug(f'Depot Endpoint : "{self.depot_endpoint}"')

    @pytest.fixture()
    def random_depot(self):
        """Return random generated depot"""

        return {
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
        }

    @pytest.fixture(scope="class")
    def random_depots(self, num_objects=20):
        """Return list of random depots"""
        return [
            {
                "latitude": random.uniform(-90, 90),
                "longitude": random.uniform(-180, 180),
            }
            for i in range(num_objects)
        ]

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
            self.depot_endpoint, headers={"Content-Type": content_type}, data=""
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
        logging.debug(f'Sending request to "{self.depot_endpoint}"')

        res: Response = client.post(
            self.depot_endpoint,
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

    def test_empty_depot(self, client):
        """Test by sending empty depot array"""

        logging.info("Testing with empty 'depots' array")

        res: Response = client.post(
            self.depot_endpoint,
            headers={"Content-Type": "application/json"},
            json={"depots": []},
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 400
        assert res.headers["Content-Type"] == "application/json"

        error_message = res.json["message"]
        assert error_message == "'depots' is empty"

    @pytest.mark.parametrize(
        "param, value",
        [
            ("latitude", -101.536),
            ("latitude", "-101.536"),
            ("latitude", -846),
            ("latitude", "-846"),
            ("latitude", 507.305),
            ("latitude", "1.04"),
            ("latitude", 643),
            ("latitude", "75"),
            ("latitude", "abl{s"),
            ("latitude", ""),
            ("longitude", -967.895),
            ("longitude", "-967.895"),
            ("longitude", -816),
            ("longitude", "-816"),
            ("longitude", 2131.114),
            ("longitude", "2131.114"),
            ("longitude", 137),
            ("longitude", "137"),
            ("longitude", "itKv{a"),
            ("longitude", ""),
        ],
    )
    def test_invalid_depot(self, client, param, value, random_depot: Dict):
        """Test with invalid parameters in depot"""

        depot = random_depot
        logging.debug(f"Depot : {depot}")

        depot[param] = value

        logging.debug(f"Invalid depot : {depot}")

        res: Response = client.post(
            self.depot_endpoint,
            headers={"Content-Type": "application/json"},
            json={"depots": [depot]},
        )

        assert res.status_code == 400
        assert f"Invalid {param}" in res.json["message"]

    def test_single_insert(self, client, random_depot: Dict):
        """Test with single depot"""

        depot = random_depot

        logging.debug(f"depot : {depot}")

        res: Response = client.post(
            self.depot_endpoint,
            headers={"Content-Type": "application/json"},
            json={"depots": [depot]},
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 201
        assert res.headers["Content-Type"] == "application/json"
        for depot, response in zip([depot], res.json["depots"]):
            id = response.pop("id")
            assert isinstance(id, int)
            assert depot == response
            response["id"] = id

    def test_multiple_insert(self, client, random_depots: List[Dict]):
        """Test with multiple objects in array"""

        logging.debug(f"Number of depots : {len(random_depots)}")

        res: Response = client.post(
            self.depot_endpoint,
            headers={"Content-Type": "application/json"},
            json={"depots": random_depots},
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 400
        assert res.headers["Content-Type"] == "application/json"
        assert "contains more than one object" in res.json["message"]

    def test_individual_get(self, client, random_depot):
        """Test by inserting depot and GET from individual resource"""

        depot = random_depot
        depots = [depot]

        logging.debug(f"Depot : {depot}")

        res: Response = client.post(
            self.depot_endpoint,
            headers={"Content-Type": "application/json"},
            json={"depots": depots},
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 201
        assert res.headers["Content-Type"] == "application/json"

        for depot, response in zip(depots, res.json["depots"]):
            id = response.pop("id")
            assert isinstance(id, int)
            assert depot == response
            response["id"] = id

            test_res = client.get(self.depot_endpoint + f"/{id}")

            logging.debug(f"Individual Response for id {id} : {test_res}")
            logging.debug(f"Individual Response Data : {test_res.data}")

            individual_depot = test_res.json
            individual_depot.pop("id")
            assert test_res.status_code == 200
            assert test_res.is_json
            assert individual_depot == depot

    def test_individual_put(self, client, random_depot):
        """Test by inserting depot and PUT from individual resource"""

        depots = [random_depot]

        logging.debug(f"Depot : {random_depot}")

        res: Response = client.post(
            self.depot_endpoint,
            headers={"Content-Type": "application/json"},
            json={"depots": depots},
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 201
        assert res.is_json

        for depot, response in zip(depots, res.json["depots"]):
            id = response.pop("id")
            assert isinstance(id, int)
            # PUT individual endpoint data
            test_res = client.put(
                self.depot_endpoint + f"/{id}",
                headers={"content-type": "application/json"},
                json=random_depot,
            )

            logging.debug(f"Individual Response for id {id} : {test_res}")
            logging.debug(f"Individual Response Data : {test_res.data}")

            assert test_res.status_code == 200
            assert test_res.is_json
            individual_depot: dict = test_res.json
            individual_depot.pop("id")
            assert individual_depot == depot
