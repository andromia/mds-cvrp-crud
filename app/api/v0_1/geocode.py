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

        if "geocodes" not in data:
            raise errors.InvalidUsage("'geocodes' missing in request data")

        geocodes = data["geocodes"]

        if not isinstance(geocodes, list):
            raise errors.InvalidUsage("'geocodes' should be a list")

        if not geocodes:
            raise errors.InvalidUsage("'geocodes' is empty")

        if "stack_id" not in data:
            raise errors.InvalidUsage("'stack_id' missing in request data")

        stack_id = data["stack_id"]

        if not stack_id:
            raise errors.InvalidUsage("'stack_id' is empty")

        for row in geocodes:
            new_geocodes = Geocode(
                zipcode=row["zipcode"],
                country=row["country"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                stack_id=stack_id,
            )

            db.session.add(new_geocodes)

        db.session.commit()

        return make_response(jsonify({"geocodes": geocodes}), 201)
