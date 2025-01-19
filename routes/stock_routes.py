from flask import Blueprint, jsonify, request
from models import db, Stock, Stock_Vectors, User_Interests
import numpy as np
from Levenshtein import distance
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

stock_bp = Blueprint('stocks', __name__)

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0  # Prevent division by zero
    return dot_product / (norm_vec1 * norm_vec2)

def compute_user_embedding(interests, embedding_dim=1153):
    """Compute the user embedding based on interests, aligning with stock embeddings."""
    # Encode interests using the SentenceTransformer model
    if not interests:
        return np.zeros(embedding_dim)  # Return a zero vector if no interests

    # Step 1: Encode text interests into embeddings
    interest_embeddings = [model.encode(interest) for interest in interests]
    text_embedding = np.mean(interest_embeddings, axis=0)  # Average interest embeddings (384 dimensions)

    # Step 2: Placeholder for numerical features (e.g., normalized market cap)
    numerical_features = np.zeros(1)  # Example: Use a single feature as a placeholder

    # Step 3: Combine embeddings
    combined_embedding = np.concatenate([numerical_features, text_embedding, text_embedding, text_embedding])
    if combined_embedding.shape[0] != embedding_dim:
        raise ValueError(f"User embedding dimension mismatch. Expected {embedding_dim}, got {combined_embedding.shape[0]}")

    return combined_embedding

@stock_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id')

    # Step 1: Fetch user interests
    user_interests = User_Interests.query.filter_by(user_id=user_id).first()
    if not user_interests or not user_interests.interests:
        return {"error": "No user interests found"}, 404

    # Step 2: Compute user embedding
    interests = user_interests.interests
    user_embedding = compute_user_embedding(interests)

    # Step 3: Fetch all stock vectors
    all_stock_vectors = Stock_Vectors.query.all()
    if not all_stock_vectors:
        return {"error": "No stock vectors found in the database"}, 404

    # Step 4: Calculate similarity for all stocks
    recommendations = []
    for stock_vector in all_stock_vectors:
        similarity = cosine_similarity(user_embedding, np.array(stock_vector.embedding))
        recommendations.append({
            "stock_id": stock_vector.stock_id,
            "similarity": similarity
        })

    # Step 5: Sort by similarity in descending order
    recommendations = sorted(recommendations, key=lambda x: x["similarity"], reverse=True)[:10]

    # Step 6: Fetch stock details for the top recommendations
    stock_ids = [rec["stock_id"] for rec in recommendations]
    recommended_stocks = Stock.query.filter(Stock.id.in_(stock_ids)).all()

    # Step 7: Format response
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

    return jsonify(sorted(response, key=lambda x: x["similarity"], reverse=True)), 200


@stock_bp.route('/search', methods=['GET'])
def search_tickers():
    query = request.args.get('query')
    if not query:
        return {"error": "Query parameter is required"}, 400

    # Fetch all tickers to calculate Levenshtein distance
    all_stocks = Stock.query.all()
    matches = []

    for stock in all_stocks:
        dist = distance(query.lower(), stock.ticker.lower())
        matches.append({
            "id": stock.id,
            "ticker": stock.ticker,
            "name": stock.name,
            "sector": stock.sector,
            "distance": dist
        })

    # Sort by distance and limit to 5 closest matches
    matches = sorted(matches, key=lambda x: x["distance"])[:5]

    # Format response without the distance field
    response = [
        {
            "id": match["id"],
            "ticker": match["ticker"],
            "name": match["name"],
            "sector": match["sector"]
        }
        for match in matches
    ]

    return jsonify(response), 200



