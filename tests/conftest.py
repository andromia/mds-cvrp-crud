from . import common
from app import create_app, db
from config import Config

import pytest
import os
import tempfile
import logging
from flask_jwt_extended import create_access_token


class TestConfig(Config):
    TESTING: bool = True


@pytest.fixture(scope="session")
def client():

    # Creating temporary file for test db
    db_fd, db_filepath = tempfile.mkstemp()

    TestConfig.SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_filepath
    logging.info(f"DB URI: {TestConfig.SQLALCHEMY_DATABASE_URI}")

    app = create_app(TestConfig)
    client = app.test_client()
    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

    # Removing temp test db
    os.close(db_fd)
    os.unlink(db_filepath)


@pytest.fixture()
def auth_header():
    app = create_app(TestConfig)

    with app.app_context():
        token: str = create_access_token(common.TEST_USER)

    header: dict = {"Authorization": "Bearer {}".format(token)}

    return header
