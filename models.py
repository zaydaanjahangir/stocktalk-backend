from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class User_Interests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # interests = db.Column(db.String(100) Is it possible to make this an array of text?
    # liked_stocks = db.Column(db.String(100), nullable=False) how to i make an array of stock_ids

class Stock(db.Model):
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

class Stock_Vectors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    # embedding VECTOR(300)

class Swipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    swipe_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
