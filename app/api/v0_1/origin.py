from . import bp, errors

from flask import request, jsonify

from app import db

from app.models import Origin


@bp.route("/origin", methods=["POST"])
def origin():
    if not request.is_json:
        raise errors.InvalidUsage("Incorrect request format! Request data must be JSON")

    data = request.get_json()

    # check_origins(data['origins'])

    if "origin" in data and data["origin"]:
        origin = data["origin"]
    else:
        raise errors.InvalidUsage("'origin' missing in request data")

    params = ["latitude", "longitude"]

    # Checking if origin is valid
    check_origin(origin)
    # Filtering the dict for safety
    origin = {param: origin[param] for param in params}

    current_origins = Origin.query.all()
    for row in current_origins:
        db.session.delete(row)

    db.session.commit()

    new_origin = Origin(**origin)
    db.session.add(new_origin)

    db.session.commit()

    origin["id"] = new_origin.id

    return jsonify({"status": "Success", "origin": origin})


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
