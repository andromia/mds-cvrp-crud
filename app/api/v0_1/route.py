from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from . import bp, errors

from app import db
from app.models import Route


@bp.route("/routes", methods=["GET", "POST"])
@jwt_required
def routes():

    if request.method == "GET":
        route = Route.query.get_or_404(1).to_dict()

        return make_response({"routes": route}, 200)

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

        if "routes" in data:
            routes = data["routes"]
        else:
            raise errors.InvalidUsage("'routes' missing in request data")

        if not isinstance(routes, dict):
            raise errors.InvalidUsage("'routes' should be a dict")

        if not routes:
            raise errors.InvalidUsage("'routes' is empty")

        routes["user_id"] = get_jwt_identity()["id"]

        # Using dict unpacking for creation
        new_routes = Route(**routes)
        db.session.add(new_routes)

        db.session.commit()

        return make_response({"routes": new_routes.to_dict()}, 201)
