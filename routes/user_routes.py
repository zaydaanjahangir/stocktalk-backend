from flask import Blueprint, request, jsonify
from models import db, User, User_Interests

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')  # Hash before saving

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User created successfully", "user_id": new_user.id}, 201


@user_bp.route('/<int:user_id>/interests', methods=['POST'])
def create_user_interests(user_id):
    data = request.json
    interests = data.get('interests')

    if not interests:
        return {"error": "Interests are required"}, 400

    new_interests = User_Interests(user_id=user_id, interests=interests)
    db.session.add(new_interests)
    db.session.commit()

    return {"message": "User interests created successfully"}, 201

@user_bp.route('/<int:user_id>/interests', methods=['PUT'])
def update_user_interests(user_id):
    data = request.json
    interests = data.get('interests')

    user_interests = User_Interests.query.filter_by(user_id=user_id).first()

    if not user_interests:
        return {"error": "User interests not found"}, 404

    user_interests.interests = interests
    db.session.commit()

    return {"message": "User interests updated successfully"}, 200

