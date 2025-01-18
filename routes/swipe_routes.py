from flask import Blueprint

swipe_bp = Blueprint('swipe', __name__)

@swipe_bp.route('/swipe', methods=['POST'])
def swipe_action():
    return {"message": "Swipe action not implemented yet"}
