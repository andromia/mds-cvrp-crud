from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from . import bp, errors

from app import db
from app.models import Stack, StackChain


@bp.route("/stack", methods=["GET", "POST"])
@jwt_required
def stack():

    if request.method == "GET":
        stacks = Stack.query.get_or_404(1).to_dict()  # TODO: can query multiple stacks

        return make_response({"stacks": [stacks]}, 200)

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

        if "stack" in data:
            stack = data["stack"]
        else:
            raise errors.InvalidUsage("'stack' missing in request data")

        if "chain" in data:
            chain = data["chain"]
        else:
            raise errors.InvalidUsage("'chain' missing in request data")

        if not isinstance(stack, dict):
            raise errors.InvalidUsage("'stack' should be a dict")

        if not isinstance(chain, list):
            raise errors.InvalidUsage("'stack' should be a list")

        if not stack:
            raise errors.InvalidUsage("'stack' is empty")

        if not chain:
            raise errors.InvalidUsage("'chain' is empty")

        stack["user_id"] = get_jwt_identity()["id"]

        # Using dict unpacking for creation
        new_stack = Stack(**stack)
        db.session.add(new_stack)

        db.session.commit()

        for st in chain:
            chained = StackChain(stack_id=new_stack.id, chained_id=st["id"])
            db.session.add(chained)

            db.session.commit()

        return make_response({"stack": new_stack.to_dict()}, 201)
