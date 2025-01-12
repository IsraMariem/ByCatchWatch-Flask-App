from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Species
from app.schemas import SpeciesSchema
from flasgger import swag_from

bp = Blueprint('species', __name__, url_prefix='/species')

# Instantiate schema
species_schema = SpeciesSchema()
speciess_schema = SpeciesSchema(many=True)

# Create a new species
@bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Species'],
    'description': 'Create a new species.',
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'African Elephant'
                    },
                    'scientific_name': {
                        'type': 'string',
                        'example': 'Loxodonta africana'
                    },
                    'conservation_status': {
                        'type': 'string',
                        'example': 'Vulnerable'
                    },
                    'region': {
                        'type': 'string',
                        'example': 'Sub-Saharan Africa'
                    }
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Species created successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'name': {
                                'type': 'string',
                                'example': 'African Elephant'
                            },
                            'scientific_name': {
                                'type': 'string',
                                'example': 'Loxodonta africana'
                            },
                            'conservation_status': {
                                'type': 'string',
                                'example': 'Vulnerable'
                            },
                            'region': {
                                'type': 'string',
                                'example': 'Sub-Saharan Africa'
                            }
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
                                'example': {'name': 'This field is required.'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def create_species():
    data = request.get_json()
    errors = species_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    new_species = Species(**data)
    db.session.add(new_species)
    db.session.commit()

    return jsonify(species_schema.dump(new_species)), 201

# Get all species
@bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Species'],
    'description': 'Retrieve a list of all species.',
    'responses': {
        '200': {
            'description': 'List of species retrieved successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {
                                    'type': 'integer',
                                    'example': 1
                                },
                                'name': {
                                    'type': 'string',
                                    'example': 'African Elephant'
                                },
                                'scientific_name': {
                                    'type': 'string',
                                    'example': 'Loxodonta africana'
                                },
                                'conservation_status': {
                                    'type': 'string',
                                    'example': 'Vulnerable'
                                },
                                'region': {
                                    'type': 'string',
                                    'example': 'Sub-Saharan Africa'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_species():
    species = Species.query.all()  # fetch all species from the database
    return jsonify(species_schema.dump(species,many=True)), 200  # use .dump() to serialize the data




@bp.route('/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Species'],
    'description': 'Update an existing species by its ID.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the species to be updated',
            'example': 1
        },
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'African Elephant'
                    },
                    'scientific_name': {
                        'type': 'string',
                        'example': 'Loxodonta africana'
                    },
                    'conservation_status': {
                        'type': 'string',
                        'example': 'Vulnerable'
                    },
                    'region': {
                        'type': 'string',
                        'example': 'Sub-Saharan Africa'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Species updated successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'name': {
                                'type': 'string',
                                'example': 'African Elephant'
                            },
                            'scientific_name': {
                                'type': 'string',
                                'example': 'Loxodonta africana'
                            },
                            'conservation_status': {
                                'type': 'string',
                                'example': 'Vulnerable'
                            },
                            'region': {
                                'type': 'string',
                                'example': 'Sub-Saharan Africa'
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Species not found.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {
                                'type': 'string',
                                'example': 'Species not found'
                            }
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
                                'example': {'name': 'This field is required.'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def update_species(id):
    data = request.get_json()
    errors = species_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    species = Species.query.get(id)  # Find the species by ID
    if not species:
        return jsonify({"error": "Species not found"}), 404

    # Update the species with the new data
    for key, value in data.items():
        setattr(species, key, value)

    db.session.commit()  # Commit the changes to the database

    return jsonify(species_schema.dump(species)), 200



@bp.route('/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Species'],
    'description': 'Delete a species by its ID.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the species to be deleted',
            'example': 1
        }
    ],
    'responses': {
        '200': {
            'description': 'Species deleted successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string',
                                'example': 'Species deleted successfully'
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Species not found.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {
                                'type': 'string',
                                'example': 'Species not found'
                            }
                        }
                    }
                }
            }
        }
    }
})
def delete_species(id):
    species = Species.query.get(id)  # Find the species by ID
    if not species:
        return jsonify({"error": "Species not found"}), 404

    db.session.delete(species)  # Delete the species from the database
    db.session.commit()  # Commit the changes to the database

    return jsonify({'message': 'Species deleted successfully'}), 200
