from flask import Blueprint, request
from models import Swipe, db

swipe_bp = Blueprint('swipes', __name__)

@swipe_bp.route('/swipe', methods=['POST'])
def swipe():
    data = request.json
    swipe = Swipe(user_id=data['userId'], stock_id=data['stockId'], swipe_type=data['swipeType'])
    db.session.add(swipe)
    db.session.commit()
    return {"message": "Swipe recorded successfully"}, 200
