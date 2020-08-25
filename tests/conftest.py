import pytest
import os
import tempfile

from config import Config

from app import create_app, db
import logging


class TestConfig(Config):
    TESTING = True


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
