from flask import Blueprint, request, jsonify
from app.extensions import db
from app.schemas import PortSchema
from flasgger import swag_from

bp = Blueprint('ports', __name__, url_prefix='/ports')

port_schema = PortSchema()
ports_schema = PortSchema(many=True)
from app.models import Port

# Create a new port
@bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Port Management'],
    'description': 'Create a new port entry with required details.',
    'parameters': [
        {
            'name': 'Port Data',
            'in': 'body',
            'description': 'The data required to create a new port, including name, location, and other relevant attributes.',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'port_name': {
                        'type': 'string',
                        'example': 'Port of Tunis'
                    },
                    'location': {
                        'type': 'string',
                        'example': 'Tunis, Tunisia'
                    },
                    'capacity': {
                        'type': 'integer',
                        'example': 5000
                    },
                    'status': {
                        'type': 'string',
                        'example': 'Active'
                    }
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Port created successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'port_name': {'type': 'string'},
                            'location': {'type': 'string'},
                            'capacity': {'type': 'integer'},
                            'status': {'type': 'string'}
                        }
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
                                'example': {'port_name': ['This field is required']}
                            }
                        }
                    }
                }
            }
        }
    }
})
def create_port():
    data = request.get_json()
    errors = port_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    new_port = Port(**data)
    db.session.add(new_port)
    db.session.commit()
    
    return port_schema.jsonify(new_port), 201

# Get all ports
@bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Port Management'],
    'description': 'Retrieve all port entries from the database.',
    'responses': {
        '200': {
            'description': 'A list of all ports in the system.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'port_name': {
                                    'type': 'string',
                                    'example': 'Port of Tunis'
                                },
                                'location': {
                                    'type': 'string',
                                    'example': 'Tunis, Tunisia'
                                },
                                'capacity': {
                                    'type': 'integer',
                                    'example': 5000
                                },
                                'status': {
                                    'type': 'string',
                                    'example': 'Active'
                                }
                            }
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Internal server error when fetching port data.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {
                                'type': 'string',
                                'example': 'An error occurred while fetching the data.'
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_ports():
    ports = Port.query.all()

    ports_data = ports_schema.dump(ports)  

    return jsonify(ports_data), 200



@bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Port Management'],
    'description': 'Update an existing port entry by its ID.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'The ID of the port to update.'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'port_name': {
                        'type': 'string',
                        'example': 'Port of Sfax'
                    },
                    'location': {
                        'type': 'string',
                        'example': 'Sfax, Tunisia'
                    },
                    'capacity': {
                        'type': 'integer',
                        'example': 4000
                    },
                    'status': {
                        'type': 'string',
                        'example': 'Inactive'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Port successfully updated.',
            'content': {
                'application/json': {
                    'schema': {
                        '$ref': '#/components/schemas/Port'
                    }
                }
            }
        },
        '400': {
            'description': 'Invalid input data or missing required fields.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'errors': {
                                'type': 'object',
                                'additionalProperties': {'type': 'array', 'items': {'type': 'string'}}
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Port with the specified ID not found.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {
                                'type': 'string',
                                'example': 'Port not found'
                            }
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Internal server error while processing the request.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {
                                'type': 'string',
                                'example': 'An error occurred while updating the port.'
                            }
                        }
                    }
                }
            }
        }
    }
})
def update_port(id):
    data = request.get_json()
    errors = port_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    port = Port.query.get(id)  
    if not port:
        return jsonify({"error": "Port not found"}), 404

    for key, value in data.items():
        setattr(port, key, value)

    db.session.commit()  
    
    return port_schema.jsonify(port), 200
