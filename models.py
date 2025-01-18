from extensions import db
from pgvector.sqlalchemy import Vector  # Correct import for VECTOR
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Enum

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class User_Interests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interests = db.Column(ARRAY(db.String), nullable=False)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(50), nullable=False)
    market_cap = db.Column(db.Float)

class Stock_Vectors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    embedding = db.Column(Vector(300), nullable=False)  # Use pgvector's Vector type

class Swipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    swipe_type = db.Column(Enum("like", "dislike", name="swipe_types"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
