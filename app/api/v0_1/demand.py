from . import bp
from . import errors

from flask import request, jsonify

from typing import Dict,Union

from app import db

from app.models import Demand, Unit


@bp.route('/demand', methods=['POST'])
def demand():

    if not request.is_json:
        raise errors.InvalidUsage("Incorrect request format! Request data must be JSON")

    data = request.get_json()

    # check_demands(data['demands'])

    if "demands" in data and data["demands"]:
        demands = data['demands']
    else:
        raise errors.InvalidUsage("'demands' missing in request data")


    params = ["latitude","longitude", "cluster_id", "unit_name", "quantity"]

    # Checking if each element is valid
    for demand in demands:

        error = check_demand(demand)
        if error:
            return error

        # Filtering the dict for safety
        demand = {param:demand[param] for param in params}

    demand_entries = []

    # Adding demands to database
    for demand in demands:
        unit = Unit.query.filter_by(name=demand['unit_name']).first()
        demand_entry = Demand(latitude=demand['latitude'],longitude=demand['longitude'],units=demand['quantity'],cluster_id=demand['cluster_id'],unit_id=unit.id)
        db.session.add(demand_entry)
        demand_entries.append(demand_entry)

    db.session.commit()

    for demand,demand_entry in zip(demands, demand_entries):
        demand['id'] = demand_entry.id

    # for unit in data['add_units']:
    #     print(f"Adding unit '{unit}'")
    #     un = Unit(name=unit)
    #     db.session.add(un)
    #     db.session.commit()


    return jsonify(demands)


def check_demand(demand:Dict[str,str]):
    """Return error in demand if any"""

    params = ["latitude","longitude", "cluster_id", "unit_name", "quantity" ]

    # Checking if all input parameters are present and are lists
    for param in params:
        if param not in demand:
            raise errors.InvalidUsage(f"Incorrect demand!", invalid_object=demand)

    # if is_float(demand['quantity']):
    #     demand['quantity'] = float(demand['quantity'])
    # else:
    #     raise errors.InvalidUsage("Invalid quantity", invalid_object=demand)

    if demand['quantity'] < 0:
        raise errors.InvalidUsage("Invalid quantity", invalid_object=demand)

    # if is_float(demand['latitude']):
    #     demand['latitude'] = float(demand['latitude'])
    # else:
    #     raise errors.InvalidUsage("Invalid latitude", invalid_object=demand)

    if demand["latitude"] < -90 or 90 < demand["latitude"]:
        raise errors.InvalidUsage("Invalid latitude", invalid_object=demand)

    # if is_float(demand['longitude']):
    #     demand['longitude'] = float(demand['longitude'])
    # else:
    #     raise errors.InvalidUsage("Invalid longitude", invalid_object=demand)

    if demand["longitude"] < -180 or 180 < demand["longitude"]:
        raise errors.InvalidUsage("Invalid longitude", invalid_object=demand)

    if is_int(demand['cluster_id']):
        demand['cluster_id'] = int(demand['cluster_id'])
    else:
        raise errors.InvalidUsage("Invalid cluster_id, should be int", invalid_object=demand)

    all_units = [unit.name for unit in Unit.query.all()]

    if demand['unit_name'] not in all_units:
        raise errors.InvalidUsage(f"Unit : {demand['unit_name']} is invalid.", invalid_object=demand)


def is_float(s:str):
    s.replace(".","",1).isdigit()


def is_int(s:str):
    try:
        int(s)
        return True
    except ValueError:
        return False
