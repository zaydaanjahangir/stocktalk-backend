from flask import Blueprint

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/stocks', methods=['GET'])
def get_stocks():
    return {"message": "Get stocks not implemented yet"}
