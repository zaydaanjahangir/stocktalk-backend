from flask import Blueprint, jsonify
from models import Stock

stock_bp = Blueprint('stocks', __name__)

@stock_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    stocks = Stock.query.limit(10).all()  # Example logic
    return jsonify([{
        "id": stock.id,
        "ticker": stock.ticker,
        "name": stock.name,
        "sector": stock.sector
    } for stock in stocks])
