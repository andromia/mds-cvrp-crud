from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from . import bp, errors

from app import db
from app.models import Geocode


@bp.route("/geocodes", methods=["GET", "POST"])
@jwt_required
def geocodes():

    if request.method == "GET":
        geocodes = Geocode.query.get_or_404(1).to_dict()

        return make_response({"geocodes": geocodes}, 200)

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

        if "geocodes" in data:
            geocodes = data["geocodes"]
        else:
            raise errors.InvalidUsage("'geocodes' missing in request data")

        if not isinstance(geocodes, dict):
            raise errors.InvalidUsage("'geocodes' should be a dict")

        if not geocodes:
            raise errors.InvalidUsage("'geocodes' is empty")

        geocodes["user_id"] = get_jwt_identity()["id"]

        # Using dict unpacking for creation
        new_geocodes = Geocode(**geocodes)
        db.session.add(new_geocodes)

        db.session.commit()

        return make_response({"geocodes": new_geocodes.to_dict()}, 201)
