from . import bp
from . import errors

from flask import request, jsonify, make_response

import logging
from typing import Dict, Union

from app import db

from app.models import Demand, Unit


@bp.route("/demand", methods=["GET", "POST"])
def demands():

    if request.method == "GET":
        return jsonify([demand.to_dict() for demand in Demand.query.all()])
        # return jsonify(Demand.query.all())

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

        if "demands" in data:
            demands = data["demands"]
        else:
            raise errors.InvalidUsage("'demands' missing in request data")

        if not demands:
            raise errors.InvalidUsage("'demands' is empty")

        params = ["latitude", "longitude", "cluster_id", "unit", "quantity"]

        # Checking if each element is valid
        for demand in demands:

            error = check_demand(demand)
            if error:
                return error

            # Filtering the dict for safety
            demand = {param: demand[param] for param in params}

        demand_entries = []

        # Adding demands to database
        for demand in demands:
            unit = Unit.query.filter_by(name=demand["unit"]).first()
            if unit is None:
                unit = Unit(name=demand["unit"])
                logging.debug(f"Created unit {unit}")
            demand_entry = Demand(
                latitude=demand["latitude"],
                longitude=demand["longitude"],
                quantity=demand["quantity"],
                cluster_id=demand["cluster_id"],
                unit=unit,
            )
            db.session.add(demand_entry)
            demand_entries.append(demand_entry)

        db.session.commit()

        for demand, demand_entry in zip(demands, demand_entries):
            demand["id"] = demand_entry.id

        # for unit in data['add_units']:
        #     print(f"Adding unit '{unit}'")
        #     un = Unit(name=unit)
        #     db.session.add(un)
        #     db.session.commit()

        return make_response(jsonify(demands), 201)


@bp.route("/demand/<int:id>", methods=["GET", "PUT"])
def demand(id):
    if request.method == "GET":
        return jsonify(Demand.query.get_or_404(id).to_dict())
    if request.method == "PUT":

        demand: Demand = Demand.query.get_or_404(id)
        if not request.is_json:
            raise errors.InvalidUsage(
                "Incorrect request format! Request data must be JSON"
            )
        data: Union[dict, None] = request.get_json(silent=True)
        if not data:
            raise errors.InvalidUsage(
                "Invalid JSON received! Request data must be JSON"
            )

        if "demand" in data:
            new_demand: dict = data["demand"]
        else:
            raise errors.InvalidUsage("'demand' missing in request data")

        # Validate demand
        check_demand(new_demand)

        # Update values in DB
        unit = Unit.query.filter_by(name=new_demand["unit"]).first()
        if unit is None:
            unit = Unit(name=new_demand["unit"])
            logging.debug(f"Created unit {unit}")

        demand.latitude = new_demand["latitude"]
        demand.longitude = new_demand["longitude"]
        demand.quantity = new_demand["quantity"]
        demand.cluster_id = new_demand["cluster_id"]
        demand.unit = unit

        db.session.commit()

        return make_response(jsonify(demand.to_dict()), 200)


def check_demand(demand: Dict[str, str]):
    """Return error in demand if any"""

    params = ["latitude", "longitude", "cluster_id", "unit", "quantity"]

    # Checking if all input parameters are present and are lists
    for param in params:
        if param not in demand:
            raise errors.InvalidUsage(f"Incorrect demand!", invalid_object=demand)

    if not is_float(demand["quantity"]) or demand["quantity"] < 0:
        if is_int(demand["quantity"]) and demand["quantity"] >= 0:
            demand["quantity"] = float(demand["quantity"])
        else:
            raise errors.InvalidUsage("Invalid quantity", invalid_object=demand)

    if not is_float(demand["latitude"]):
        raise errors.InvalidUsage("Invalid latitude", invalid_object=demand)
    if demand["latitude"] < -90 or 90 < demand["latitude"]:
        raise errors.InvalidUsage("Invalid latitude", invalid_object=demand)

    if not is_float(demand["longitude"]):
        raise errors.InvalidUsage("Invalid longitude", invalid_object=demand)

    if demand["longitude"] < -180 or 180 < demand["longitude"]:
        raise errors.InvalidUsage("Invalid longitude", invalid_object=demand)

    if not is_int(demand["cluster_id"]) or demand["cluster_id"] < 0:
        raise errors.InvalidUsage(
            "Invalid cluster_id, should be int", invalid_object=demand
        )

    if not is_string(demand["unit"]) or not demand["unit"].isalpha():
        raise errors.InvalidUsage(
            f"Invalid unit, should be string with letters only.", invalid_object=demand
        )


def is_float(x: any):
    return isinstance(x, float)


def is_int(x: any):
    return isinstance(x, int)


def is_string(x: any):
    return isinstance(x, str)
