from . import bp, errors
from app import db
from app.models import Route

from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging


@bp.route("/route", methods=["GET", "POST"])
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

        if "routes" not in data:
            raise errors.InvalidUsage("'routes' missing in request data")

        routes = data["routes"]

        if not isinstance(routes, list):
            raise errors.InvalidUsage("'routes' should be a list")

        if not routes:
            raise errors.InvalidUsage("'routes' is empty")

        if "stack_id" not in data:
            raise errors.InvalidUsage("'stack_id' missing in request data")

        stack_id = data["stack_id"]

        if not stack_id:
            raise errors.InvalidUsage("'stack_id' is empty")

        for row in routes:
            route_entry = Route(
                demand_id=row["demand_id"],
                depot_id=row["depot_id"],
                vehicle_id=row["vehicle_id"],
                stop_number=row["stop_number"],
                stack_id=stack_id,
            )

            db.session.add(route_entry)

        db.session.commit()

        return make_response(jsonify({"routes": routes}), 201)
