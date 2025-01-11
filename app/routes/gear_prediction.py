
from flask import Blueprint, jsonify, request
from app.gear_type_solution_prediction import get_recommended_gear

gear_bp = Blueprint('gear_recommendation', __name__)

@gear_bp.route('/recommend_gear', methods=['POST'])
def recommend_gear():
    data = request.get_json()
    species_name = data.get('species')
    region = data.get('region')
    
    gear_recommendation = get_recommended_gear(species_name, region)
    
    return jsonify({'recommended_gear': gear_recommendation})

