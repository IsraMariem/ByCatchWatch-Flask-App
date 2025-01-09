from flask import Blueprint, jsonify
from app.recommendation_logic import generate_recommendations
from app.models import Recommendation

bp_recom = Blueprint('recommendations', __name__)

@bp_recom.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    """
    Generate and retrieve recommendations for a specific user.
    """
    # Generate recommendations for the user
    result = generate_recommendations(user_id)

    # If no user is found or no recommendations are generated, return an appropriate message
    if isinstance(result, str):  # This handles the "User not found" or "No recommendations generated" case
        return jsonify({'message': result}), 404

    # Retrieve the user's recommendations from the database
    recommendations = Recommendation.query.filter_by(user_id=user_id).all()

    # Return recommendations as a JSON response
    return jsonify([{'content': rec.content} for rec in recommendations]), 200











"""from flask import Blueprint, jsonify
from app.recommendation_logic import generate_recommendations
from app.models import Recommendation

bp_recom= Blueprint('recommendations', __name__)

@bp_recom.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    # Generate recommendations for the user
    generate_recommendations(user_id)

    # Retrieve the user's recommendations from the database
    recommendations = Recommendation.query.filter_by(user_id=user_id).all()

    # Return recommendations as a JSON response
    return jsonify([{'content': rec.content} for rec in recommendations])"""
