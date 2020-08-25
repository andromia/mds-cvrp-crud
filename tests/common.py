from flask_jwt_extended import create_access_token

from app import create_app, __version__
from config import Config


BASE_URL: str = f"/api/{__version__}"


class TestConfig(Config):
    TESTING = True


def create_auth_headers():
    app = create_app(TestConfig)

    with app.app_context():
        token = create_access_token("test")

    headers = {"Authorization": "Bearer {}".format(token)}

    return headers


AUTH_HEADER = create_auth_headers()
