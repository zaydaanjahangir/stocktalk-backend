from flask import Blueprint, jsonify, request
from models import db, Stock, Stock_Vectors, User_Interests
import numpy as np

stock_bp = Blueprint('stocks', __name__)

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0  # Prevent division by zero
    return dot_product / (norm_vec1 * norm_vec2)

@stock_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id')
    
    # Fetch user interests
    user_interests = User_Interests.query.filter_by(user_id=user_id).first()
    if not user_interests or not user_interests.interests:
        return {"error": "No user interests found"}, 404

    # Generate a dummy embedding for the user
    user_embedding = np.random.rand(1153)  # Example placeholder

    # Fetch all stock vectors
    all_stock_vectors = Stock_Vectors.query.all()
    if not all_stock_vectors:
        return {"error": "No stock vectors found in the database"}, 404

    # Calculate similarity for all stocks
    recommendations = []
    for stock_vector in all_stock_vectors:
        similarity = cosine_similarity(user_embedding, np.array(stock_vector.embedding))
        recommendations.append({
            "stock_id": stock_vector.stock_id,
            "similarity": similarity
        })

    # Sort by similarity in descending order
    recommendations = sorted(recommendations, key=lambda x: x["similarity"], reverse=True)[:10]

    # Fetch stock details for the top recommendations
    stock_ids = [rec["stock_id"] for rec in recommendations]
    recommended_stocks = Stock.query.filter(Stock.id.in_(stock_ids)).all()

    # Format response
    response = [
        {
            "id": stock.id,
            "ticker": stock.ticker,
            "name": stock.name,
            "sector": stock.sector,
            "similarity": next((rec["similarity"] for rec in recommendations if rec["stock_id"] == stock.id), 0)
        }
        for stock in recommended_stocks
    ]

    # Sort the final response by similarity
    response = sorted(response, key=lambda x: x["similarity"], reverse=True)

    return jsonify(response), 200



