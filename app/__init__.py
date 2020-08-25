import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy, orm
from flask_migrate import Migrate
from config import Config

__version__ = "v0.1"

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.api.v0_1 import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api/v0.1")

    return app
