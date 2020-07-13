from . import bp, errors

from flask import request, jsonify, make_response

import logging
from typing import Dict, Union

from app import db

from app.models import Origin, Unit


@bp.route("/origin", methods=["GET", "POST"])
def origins():

    if request.method == "GET":
        origin = Origin.query.get_or_404(1).to_dict()
        return jsonify({"origin": origin})

    if request.method == "POST":

        if not request.is_json:
            raise errors.InvalidUsage(
                "Incorrect request format! Request data must be JSON"
            )

        data = request.get_json(silent=True)
        if not data:
            raise errors.InvalidUsage(
                "Invalid JSON received! Request data must be JSON"
            )

        if "origins" in data:
            origins = data["origins"]
        else:
            raise errors.InvalidUsage("'origins' missing in request data")

        if not isinstance(origins, list):
            raise errors.InvalidUsage("'origins' should be list")

        if not origins:
            raise errors.InvalidUsage("'origins' is empty")
        elif len(origins) != 1:
            raise errors.InvalidUsage("'origins' contains more than one object")

        origin = origins[0]

        # Checking if origin is valid
        check_origin(origin)

        # Deleting every origin
        Origin.query.delete()

        # Filtering the dict
        params = ["latitude", "longitude"]
        origin = {param: origin[param] for param in params}

        # Using dict unpacking for creation
        new_origin = Origin(**origin)
        db.session.add(new_origin)

        db.session.commit()

        origin["id"] = new_origin.id

        return make_response(jsonify({"origins": [origin]}), 201)


@bp.route("/origin/<int:id>", methods=["GET", "PUT"])
def origin(id: int):
    if request.method == "GET":
        return Origin.query.get_or_404(id).to_dict()
    if request.method == "PUT":

        origin: Origin = Origin.query.get_or_404(id)

        if not request.is_json:
            raise errors.InvalidUsage(
                "Incorrect request format! Request data must be JSON"
            )

        data: Union[dict, None] = request.get_json(silent=True)
        if not data:
            raise errors.InvalidUsage(
                "Invalid JSON received! Request data must be JSON"
            )

        params = ["latitude", "longitude"]

        new_origin: Dict[str, any] = {}

        for param in params:
            if param in data:
                new_origin[param] = data[param]
            else:
                raise errors.InvalidUsage(f"{param} missing in request data")

        # Validate new data
        check_origin(new_origin)

        # Update values in DB
        origin.latitude = new_origin["latitude"]
        origin.longitude = new_origin["longitude"]

        db.session.commit()

        return make_response(jsonify(origin.to_dict()), 200)


def check_origin(origin):
    params = ["latitude", "longitude"]

    # Checking if all input parameters are present
    for param in params:
        if param not in origin:
            raise errors.InvalidUsage("Incorrect origin!", invalid_object=origin)

    if not is_float(origin["latitude"]):
        raise errors.InvalidUsage("Invalid latitude", invalid_object=origin)

    if origin["latitude"] < -90 or 90 < origin["latitude"]:
        raise errors.InvalidUsage("Invalid latitude", invalid_object=origin)

    if not is_float(origin["longitude"]):
        raise errors.InvalidUsage("Invalid longitude", invalid_object=origin)

    if origin["longitude"] < -180 or 180 < origin["longitude"]:
        raise errors.InvalidUsage("Invalid longitude", invalid_object=origin)


def is_float(x: any):
    return isinstance(x, float)
