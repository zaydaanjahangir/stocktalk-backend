from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    return {"message": "Login not implemented yet"}
