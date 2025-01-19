from flask import Blueprint, request, jsonify
from models import db, Swipe, User_Interests

swipe_bp = Blueprint('swipes', __name__)

@swipe_bp.route('/swipe', methods=['POST'])
def record_swipe():
    data = request.json
    user_id = data.get('user_id')
    stock_id = data.get('stock_id')
    swipe_type = data.get('swipe_type')  # "like" or "dislike"

    if not user_id or not stock_id or not swipe_type:
        return {"error": "user_id, stock_id, and swipe_type are required"}, 400

    new_swipe = Swipe(user_id=user_id, stock_id=stock_id, swipe_type=swipe_type)
    db.session.add(new_swipe)

    # Update liked stocks for "like" swipes
    if swipe_type == "like":
        user_interests = User_Interests.query.filter_by(user_id=user_id).first()
        if user_interests:
            user_interests.liked_stocks.append(stock_id)

    db.session.commit()

    return {"message": "Swipe recorded successfully"}, 201
