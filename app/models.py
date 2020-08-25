from werkzeug.security import generate_password_hash

from app import db
from app.utils import timestamp


def create_fk(identifier: str, nullable: bool = False):
    return db.Column(db.Integer, db.ForeignKey(identifier), nullable=nullable)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class Depot(db.Model):
    """
    Depot defined by users. 
      - origin identifier
      - latitude
      - longitude
    """

    __tablename__ = "depots"

    def __repr__(self):
        return f"<Depot id='{self.id}' coordinates=({self.latitude},{self.longitude})>"

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "user_id": self.user_id,
        }

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_id = create_fk("users.id")


class Demand(db.Model):
    """
    Demand is a destination node to be routed.
      - demand identifier (pk)
      - geocodes (latitude & longitude)
      - units for capacity constraint
      - cluster identifier for sub-problem spaces
    """

    __tablename__ = "demand"

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "unit": self.unit,
            "quantity": self.quantity,
            "cluster_id": self.cluster_id,
            "user_id": self.user_id,
        }

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10))
    cluster_id = db.Column(db.Integer)
    user_id = create_fk("users.id")


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
        return f"<Vehicle id='{self.id}' capacity='{self.capacity} {self.unit.name}'>"

    def to_dict(self):
        return {
            "id": self.id,
            "capacity": self.capacity,
            "unit": self.unit,
            "user_id": self.user_id,
        }

    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Float, nullable=False)
    user_id = create_fk("users.id")


class Route(db.Model):
    """
    Routes are results along with their mappings to resources used
    to produce them.
        - demand identifier
        - depot identifier
        - vehicle identifier
        - stop number
    """

    __tablename__ = "routes"

    def to_dict(self):
        return {
            "id": self.id,
            "demand": self.demand.to_dict,
            "depot": self.depot.to_dict,
            "vehicle": self.vehicle,
            "stop_number": self.stop_number,
            "user_id": self.user_id,
        }

    id = db.Column(db.Integer, primary_key=True)
    demand_id = create_fk("demand.id")
    depot_id = create_fk("depots.id")
    vehicle_id = create_fk("vehicles.id")
    stop_number = db.Column(db.Integer, nullable=False)
    user = create_fk("users.id")
