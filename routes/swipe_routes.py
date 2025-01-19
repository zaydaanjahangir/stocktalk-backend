from flask import Blueprint, request, jsonify
from models import db, Swipe, User_Interests, Stock

swipe_bp = Blueprint('swipes', __name__)

@swipe_bp.route('/swipe', methods=['POST'])
def record_swipe():
    data = request.json
    user_id = data.get('user_id')
    stock_id = data.get('stock_id')
    swipe_type = data.get('swipe_type')  # "like" or "dislike"

    # Validate required data
    if not user_id or not stock_id or not swipe_type:
        return {"error": "user_id, stock_id, and swipe_type are required"}, 400

    # Check if the swipe already exists for this user and stock
    existing_swipe = Swipe.query.filter_by(user_id=user_id, stock_id=stock_id).first()
    if existing_swipe:
        return {"error": "You have already swiped on this stock"}, 409

    # Record the swipe
    new_swipe = Swipe(user_id=user_id, stock_id=stock_id, swipe_type=swipe_type)
    db.session.add(new_swipe)

    # If "like", add stock categories to user's interests
    if swipe_type == "like":
        user_interests = User_Interests.query.filter_by(user_id=user_id).first()
        stock = Stock.query.get(stock_id)

        if not user_interests:
            return {"error": "User interests not found"}, 404
        if not stock:
            return {"error": "Stock not found"}, 404

        # Add unique categories from the stock to the user's interests
        new_categories = set(stock.categories or [])  # Handle None categories
        existing_interests = set(user_interests.interests)
        updated_interests = list(existing_interests.union(new_categories))

        # Update the database
        user_interests.interests = updated_interests

    db.session.commit()

    return {"message": "Swipe recorded successfully"}, 201
