from flask import Blueprint, request, jsonify
from app.extensions import db
from flasgger import swag_from
from flask_login import login_required
bp = Blueprint('bycatch', __name__, url_prefix='/bycatch')


from app.schemas import BycatchStatSchema

bycatch_schema = BycatchStatSchema()
bycatchs_schema = BycatchStatSchema(many=True)

from app.models import Bycatch

# Create a new Bycatch
@bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Bycatch'],
    'description': 'Create a new bycatch entry.',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'species_id': {'type': 'integer', 'example': 1},
                        'port_id': {'type': 'integer', 'example': 2},
                        'quantity': {'type': 'integer', 'example': 10},
                        'date': {'type': 'string', 'format': 'date', 'example': '2025-01-12'}
                    },
                    'required': ['species_id', 'port_id', 'quantity', 'date']
                }
            }
        }
    },
    'responses': {
        '201': {
            'description': 'Bycatch entry created successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/Bycatch'
                    }
                }
            }
        },
        '400': {
            'description': 'Invalid input data.',
            'content': {
                'application/json': {
                    'example': {
                        'errors': {
                            'species_id': 'Field may not be null.',
                            'quantity': 'Must be a positive integer.'
                        }
                    }
                }
            }
        }
    }
})
@login_required
def create_bycatch():
    data = request.get_json() 
    errors = bycatch_schema.validate(data) 
    if errors:
        return jsonify({"errors": errors}), 400  

    new_bycatch = Bycatch(**data) 
    db.session.add(new_bycatch)  
    db.session.commit()  

    return bycatch_schema.jsonify(new_bycatch), 201 

# Get all bycatch records
@bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Bycatch'],
    'description': 'Retrieve all bycatch records.',
    'responses': {
        '200': {
            'description': 'A list of all bycatch records.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            '$ref': '#/components/schemas/Bycatch'
                        }
                    }
                }
            }
        }
    }
})
def get_bycatch():
    bycatch = Bycatch.query.all()  
    return jsonify(bycatch_schema.dump(bycatch, many=True)), 200  


# Partial Update a Bycatch record (PATCH)
@bp.route('/<string:id>', methods=['PATCH'])
@swag_from({
    'tags': ['Bycatch'],
    'description': 'Partially update a bycatch record by its ID.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'The ID of the bycatch record to update.',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'body',
            'in': 'body',
            'description': 'The fields to update for the bycatch record.',
            'required': True,
            'schema': {
                '$ref': '#/components/schemas/Bycatch'
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Successfully updated the bycatch record.',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/Bycatch'
                    }
                }
            }
        },
        '400': {
            'description': 'Invalid input data.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'errors': {
                                'type': 'object',
                                'additionalProperties': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Bycatch record not found.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        }
    }
})
@login_required
def partial_update_bycatch(id):
    data = request.get_json()  
    errors = bycatch_schema.validate(data)  
    if errors:
        return jsonify({"errors": errors}), 400

    
    bycatch = Bycatch.query.get(id)
    if not bycatch:
        return jsonify({"error": "Bycatch not found"}), 404

  
    for key, value in data.items():
        if hasattr(bycatch, key):  
            setattr(bycatch, key, value) 

    db.session.commit()  

    return jsonify(bycatch_schema.dump(bycatch)), 200
