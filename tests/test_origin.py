import pytest
import logging
import json

import random
import string

from typing import List, Dict

# from flask import FlaskClient
from werkzeug.wrappers import Response


class TestOrigin:
    @pytest.fixture(autouse=True)
    def set_origin_endpoint(self, api_base_url):
        """Set origin endpoint as object variable"""

        self.origin_endpoint: str = api_base_url + "/origin"
        logging.debug(f'Origin Endpoint : "{self.origin_endpoint}"')

    @pytest.fixture()
    def random_origin(self):
        """Return random generated origin"""

        return {
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
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
            self.origin_endpoint, headers={"Content-Type": content_type}, data=""
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
        logging.debug(f'Sending request to "{self.origin_endpoint}"')

        res: Response = client.post(
            self.origin_endpoint,
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

    def test_empty_origin(self, client):
        """Test by sending empty origin array"""

        logging.info("Testing with empty 'origins' array")

        res: Response = client.post(
            self.origin_endpoint,
            headers={"Content-Type": "application/json"},
            json={"origins": []},
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 400
        assert res.headers["Content-Type"] == "application/json"

        error_message = res.json["message"]
        assert error_message == "'origins' is empty"

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
    def test_invalid_origin(self, client, param, value, random_origin: Dict):
        """Test with invalid parameters in origin"""

        origin = random_origin
        logging.debug(f"Origin : {origin}")

        origin[param] = value

        logging.debug(f"Invalid origin : {origin}")

        res: Response = client.post(
            self.origin_endpoint,
            headers={"Content-Type": "application/json"},
            json={"origins": [origin]},
        )

        assert res.status_code == 400
        assert f"Invalid {param}" in res.json["message"]

    def test_single_insert(self, client, random_origin: Dict):
        """Test with single origin"""

        origin = random_origin

        logging.debug(f"origin : {origin}")

        res: Response = client.post(
            self.origin_endpoint,
            headers={"Content-Type": "application/json"},
            json={"origins": [origin]},
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 201
        assert res.headers["Content-Type"] == "application/json"
        for origin, response in zip([origin], res.json["origins"]):
            id = response.pop("id")
            assert isinstance(id, int)
            assert origin == response
            response["id"] = id
