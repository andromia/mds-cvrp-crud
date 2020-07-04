from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from . import bp


class InvalidUsage(Exception):
    status_code = 400

    def __init__(
        self,
        message: str,
        status_code: int = None,
        payload=None,
        invalid_object: any = None,
    ):
        Exception.__init__(self)
        self.message = message
        self.invalid_object = invalid_object
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        if self.invalid_object is not None:
            rv["invalid_object"] = self.invalid_object
        return rv


@bp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def error_response(status_code: int, message: str = None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message: str):
    return error_response(400, message)
