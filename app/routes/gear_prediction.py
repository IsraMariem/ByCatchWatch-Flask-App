
from flask import Blueprint, jsonify, request
from app.gear_type_solution_prediction import get_recommended_gear
from flasgger import swag_from
gear_bp = Blueprint('gear_recommendation', __name__)

@gear_bp.route('/recommend_gear', methods=['POST'])
@swag_from({
    'tags': ['Gear Recommendation'],
    'description': 'Recommend fishing gear based on species and region.',
    'parameters': [
        {
            'name': 'species',
            'in': 'body',
            'description': 'The species for which to recommend fishing gear.',
            'required': True,
            'schema': {
                'type': 'string',
                'example': 'Tuna'
            }
        },
        {
            'name': 'region',
            'in': 'body',
            'description': 'The region where the fishing will take place.',
            'required': True,
            'schema': {
                'type': 'string',
                'example': 'North Atlantic'
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Recommended fishing gear based on species and region.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'recommended_gear': {
                                'type': 'string',
                                'example': 'Longline, J-hook, Monofilament line'
                            }
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Missing or invalid input data.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def recommend_gear():
    data = request.get_json()
    species_name = data.get('species')
    region = data.get('region')
    
    gear_recommendation = get_recommended_gear(species_name, region)
    
    return jsonify({'recommended_gear': gear_recommendation})

