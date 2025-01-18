from flask import Blueprint, jsonify
from app.recommendation_logic import generate_recommendations
from app.models import Recommendation
from flasgger import swag_from

bp_recom = Blueprint('recommendations', __name__)

@bp_recom.route('/recommendations/<int:user_id>', methods=['GET'])
@swag_from({
    'tags': ['Recommendations'],
    'description': 'Generate and retrieve recommendations for a specific user.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the user for whom to generate and retrieve recommendations.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successfully retrieved user recommendations.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'content': {
                                    'type': 'string',
                                    'example': 'Recommendation content for the user.'
                                }
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'User not found or no recommendations generated.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'example': 'User not found'  
                            }
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Internal server error while retrieving recommendations.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {
                                'type': 'string',
                                'example': 'An error occurred while retrieving recommendations.'
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_recommendations(user_id):
    """
    Generate and retrieve recommendations for a specific user.
    """
    result = generate_recommendations(user_id)

    if isinstance(result, str):  
        return jsonify({'message': result}), 404

    recommendations = Recommendation.query.filter_by(user_id=user_id).all()

    return jsonify([{'content': rec.content} for rec in recommendations]), 200


