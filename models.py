from app import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import VECTOR
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
    __table_args__ = (
        db.UniqueConstraint('ticker', name='unique_ticker'),
        db.CheckConstraint('market_cap >= 0', name='positive_market_cap'),
    )
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(50), nullable=False)
    market_cap = db.Column(db.Float)
    year_high = db.Column(db.Float)
    year_low = db.Column(db.Float)
    daily_high = db.Column(db.Float)
    daily_low = db.Column(db.Float)
    daily_open = db.Column(db.Float)
    price_earnings_ratio = db.Column(db.Float)
    dividend_yield = db.Column(db.Float)

class LikedStocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)

class Stock_Vectors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    embedding = db.Column(VECTOR(300), nullable=False)

class Swipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    swipe_type = db.Column(Enum("like", "dislike", name="swipe_types"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
