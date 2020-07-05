from .utils import timestamp

from app import db, orm


def create_fk(identifier: str, nullable: bool = False):
    return db.Column(db.Integer, db.ForeignKey(identifier), nullable=nullable)


class Unit(db.Model):
    """
    Units are unit of measure resources. For example, 'pallets', 'pounds', 'haversine miles', etc.
      - unit of measure identifier (pk)
      - unit of measure string
    """

    __tablename__ = "units"

    def __repr__(self):
        return f"<Unit id='{self.id}' name='{self.name}'>"

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


class Origin(db.Model):
    """
    Origins defined by users. 
      - origin identifier
      - latitude
      - longitude
    """

    __tablename__ = "origins"

    def __repr__(self):
        return f"<Origin id='{self.id}' coordinates=({self.latitude},{self.longitude})>"

    def to_dict(self):
        return {"id": self.id, "latitude": self.latitude, "longitude": self.longitude}

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


class Demand(db.Model):
    """
    Demand is a destination node to be routed.
      - demand identifier (pk)
      - geocodes (latitude & longitude)
      - units for capacity constraint
      - unit identifier (fk)
      - cluster identifier for sub-problem spaces
    """

    __tablename__ = "demands"

    def __repr__(self):
        return f"<Demand id='{self.id}'coordinates=({self.latitude},{self.longitude}) quantity='{self.units} {self.unit.name}' cluster_id='{self.cluster_id}'>"

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "unit": self.unit.name,
            "quantity": self.units,
            "cluster_id": self.cluster_id,
        }

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    units = db.Column(db.Float, nullable=False)
    unit_id = create_fk("unit.id")
    unit = orm.relationship("Unit")
    cluster_id = db.Column(db.Integer)


class Vehicle(db.Model):
    """
    Vehicle is defined by capacity and other configurables to be used.
      - vehicle identifier (pk)
      - max capacity constraint
      - unit identifier (fk)
      - asset class identifier (fk)
    """

    __tablename__ = "vehicles"

    def __repr__(self):
        return f"<Vehicle id='{self.id}' capacity='{self.max_capacity_units} {self.unit.name}'>"

    def to_dict(self):
        return {
            "id": self.id,
            "max_capacity_units": self.max_capacity_units,
            "unit": self.unit,
        }

    id = db.Column(db.Integer, primary_key=True)
    max_capacity_units = db.Column(db.Float, nullable=False)
    unit_id = create_fk("unit.id")
    unit = orm.relationship("Unit")


class Solution(db.Model):
    """
    Solutions are results along with their mappings to resources used
    to produce them.
        - demand identifier
        - origin identifier
        - stop identifier
        - output data
    """

    __tablename__ = "solutions"

    def __repr__(self):
        return f"<Solution id='{self.id}' origin=({self.origin.latitude},{self.origin.longitude}) demand_location=({self.demand.latitude},{self.demand.longitude}) vehicle='{self.vehicle.id}' stop number {self.stop_num} at {self.stop_distance_units} {self.unit.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "demand": self.demand.to_dict,
            "origin": self.origin.to_dict,
            "vehicle": self.vehicle,
            "stop_num": self.stop_num,
            "stop_distance_units": self.stop_distance_units,
            "unit": self.unit.name,
        }

    id = db.Column(db.Integer, primary_key=True)
    demand_id = create_fk("demand.id")
    demand = orm.relationship("Demand")
    origin_id = create_fk("origin.id")
    origin = orm.relationship("Origin")
    vehicle_id = create_fk("vehicle.id")
    vehicle = orm.relationship("Vehicle")
    stop_num = db.Column(db.Integer, nullable=False)
    stop_distance_units = db.Column(db.Float, nullable=False)
    unit_id = create_fk("unit.id")
    unit = orm.relationship("Unit")
