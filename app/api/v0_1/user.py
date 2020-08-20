from . import bp, errors

from flask import request, jsonify, make_response

import logging
from typing import Dict, Union

from app import db

from app.models import User


@bp.route("/user", methods=["GET", "POST"])
def user():

    if request.method == "GET":
        user = User.query.get_or_404(1).to_dict()
        return jsonify({"user": user})

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

        if "user" in data:
            user = data["user"]
        else:
            raise errors.InvalidUsage("'user' missing in request data")

        if not isinstance(user, dict):
            raise errors.InvalidUsage("'user' should be a dict")

        if not user:
            raise errors.InvalidUsage("'user' is empty")
        elif len(user) > 1:
            raise errors.InvalidUsage("'user' contains more than one object")

        # Using dict unpacking for creation
        new_user = User(**user)
        db.session.add(new_user)

        db.session.commit()

        user["id"] = new_user.id

        return make_response(jsonify({"user": [user]}), 201)


@bp.route("/user/<int:id>", methods=["GET", "PUT"])
def user_one(id: int):
    if request.method == "GET":
        return User.query.get_or_404(id).to_dict()
    if request.method == "PUT":

        user: User = User.query.get_or_404(id)

        if not request.is_json:
            raise errors.InvalidUsage(
                "Incorrect request format! Request data must be JSON"
            )

        data: Union[dict, None] = request.get_json(silent=True)
        if not data:
            raise errors.InvalidUsage(
                "Invalid JSON received! Request data must be JSON"
            )

        params = ["username", "password"]

        new_user: Dict[str, any] = {}

        for param in params:
            if param in data:
                new_user[param] = data[param]
            else:
                raise errors.InvalidUsage(f"{param} missing in request data")

        # Update values in DB
        user.username = new_user["latitude"]
        user.set_password(new_user["password"])

        db.session.commit()

        return make_response(jsonify(user.to_dict()), 200)
