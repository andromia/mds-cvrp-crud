from . import bp, errors

from flask import request, jsonify, make_response

from app import db

from app.models import Origin


@bp.route("/origin", methods=["GET", "POST"])
def origin():

    if request.method == "GET":
        origin = Origin.query.get_or_404(1).to_dict()
        return jsonify({"origin": origin})

    if request.method == "POST":

        if not request.is_json:
            raise errors.InvalidUsage(
                "Incorrect request format! Request data must be JSON"
            )

        data = request.get_json()

        if "origin" in data:
            origin = data["origin"]
        else:
            raise errors.InvalidUsage("'origin' missing in request data")

        if not isinstance(origin, list):
            raise errors.InvalidUsage("'origin' should be list")

        if not origin:
            raise errors.InvalidUsage("'origin' is empty")
        elif len(origin) != 1:
            raise errors.InvalidUsage("'origin' contains more than one object")

        origin = origin[0]

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

        return make_response(jsonify({"origin": origin}), 201)


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
