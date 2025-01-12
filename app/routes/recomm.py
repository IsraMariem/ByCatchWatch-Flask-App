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
                                'example': 'User not found'  # Can also be 'No recommendations generated'
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
    # Generate recommendations for the user
    result = generate_recommendations(user_id)

    # If no user is found or no recommendations are generated, return an appropriate message
    if isinstance(result, str):  # This handles the "User not found" or "No recommendations generated" case
        return jsonify({'message': result}), 404

    # Retrieve the user's recommendations from the database
    recommendations = Recommendation.query.filter_by(user_id=user_id).all()

    # Return recommendations as a JSON response
    return jsonify([{'content': rec.content} for rec in recommendations]), 200


