from flask import Blueprint, jsonify
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
    return jsonify([{'content': rec.content} for rec in recommendations])
