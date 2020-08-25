from werkzeug.security import generate_password_hash

from app import db
from app.utils import timestamp


def create_fk(identifier: str, nullable: bool = False):
    return db.Column(db.Integer, db.ForeignKey(identifier), nullable=nullable)


class User(db.Model):
    """
    User data.
      - user identifier
      - username
      - email
      - password hash
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class Stack(db.Model):
    """
    solverstack unique Stacks created.
      - stack identifier
      - stack name
      - user identifier
    """

    __tablename__ = "stacks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    user_id = create_fk("users.id")

    def __repr__(self):
        return f"<Stack {self.name}>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "user_id": self.user_id}


class StackChain(db.Model):
    """
    Relationship detail on solverstack Stacks.
      - chain identifier
      - stack identifier
      - chained stack identifier
    """

    __tablename__ = "chained_stacks"

    id = db.Column(db.Integer, primary_key=True)
    stack_id = create_fk("stacks.id")
    chained_id = create_fk("stacks.id")

    def __repr__(self):
        return f"<StackChain ({self.stack_id, self.chained_id})>"

    def to_dict(self):
        return {"id": self.id, "stack_id": self.stack_id, "chained_id": self.chained_id}


class Geocode(db.Model):
    """
    Location data with latitudes and longitudes.
      - location identifier
      - zipcode
      - country
      - latitude
      - longitude
      - user identifier
    """

    __tablename__ = "geocodes"

    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String(5), nullable=False)
    country = db.Column(db.String(2), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_id = create_fk("users.id")

    def __repr__(self):
        return (
            f"<Geocode id='{self.id}' "
            "zipcode='{self.zipcode}' "
            "country='{self.country}' "
            "coordinates=({self.latitude},{self.longitude})>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "zipcode": self.zipcode,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


class Depot(db.Model):
    """
    Depot defined by users. 
      - depot identifier
      - latitude
      - longitude
      - user identifier
    """

    __tablename__ = "depots"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_id = create_fk("users.id")

    def __repr__(self):
        return (
            f"<Depot id='{self.id}' " "coordinates=({self.latitude},{self.longitude})>"
        )

    def to_dict(self):
        return {"id": self.id, "latitude": self.latitude, "longitude": self.longitude}


class Demand(db.Model):
    """
    Demand is a destination node to be routed.
      - demand identifier (pk)
      - geocodes (latitude & longitude)
      - units for capacity constraint
      - cluster identifier for sub-problem spaces
      - user identifier
    """

    __tablename__ = "demand"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10))
    cluster_id = db.Column(db.Integer)
    user_id = create_fk("users.id")

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "unit": self.unit,
            "quantity": self.quantity,
            "cluster_id": self.cluster_id,
        }


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

    id = db.Column(db.Integer, primary_key=True)
    demand_id = create_fk("demand.id")
    depot_id = create_fk("depots.id")
    vehicle_id = db.Column(db.Integer)
    stop_number = db.Column(db.Integer)
    user_id = create_fk("users.id")

    def to_dict(self):
        return {
            "id": self.id,
            "demand": self.demand_id,
            "depot": self.depot_id,
            "vehicle_id": self.vehicle_id,
            "stop_number": self.stop_number,
        }
