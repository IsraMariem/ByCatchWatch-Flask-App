from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Report
from app.schemas import ReportSchema
from flasgger import swag_from

bp = Blueprint('reports', __name__, url_prefix='/reports')


report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)

from flask_login import login_required

# Add new report
@bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Reports'],
    'description': 'Create a new report.',
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string',
                        'example': 'Annual Sales Report'
                    },
                    'content': {
                        'type': 'string',
                        'example': 'The content of the annual sales report.'
                    }
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Successfully created a new report.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'title': {
                                'type': 'string',
                                'example': 'Annual Sales Report'
                            },
                            'content': {
                                'type': 'string',
                                'example': 'The content of the annual sales report.'
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
                                'example': {'title': 'This field is required.'}
                            }
                        }
                    }
                }
            }
        }
    }
})
@login_required
def create_report():
    data = request.get_json()
    errors = report_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    new_report = Report(**data)
    db.session.add(new_report)
    db.session.commit()

    return jsonify(report_schema.dump(new_report)), 201 


# Get all reports
@bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Reports'],
    'description': 'Retrieve all reports.',
    'responses': {
        '200': {
            'description': 'Successfully retrieved all reports.',
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
                                'title': {
                                    'type': 'string',
                                    'example': 'Annual Sales Report'
                                },
                                'content': {
                                    'type': 'string',
                                    'example': 'The content of the annual sales report.'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_reports():
    reports = Report.query.all()  
    return jsonify(reports_schema.dump(reports, many=True)), 200 

@bp.route('/<int:id>', methods=['PUT'])
@login_required
@swag_from({
    'tags': ['Reports'],
    'description': 'Update an existing report by its ID.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the report to update'
        },
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string',
                        'example': 'Updated Sales Report'
                    },
                    'content': {
                        'type': 'string',
                        'example': 'The updated content of the sales report.'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Successfully updated the report.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'title': {
                                'type': 'string',
                                'example': 'Updated Sales Report'
                            },
                            'content': {
                                'type': 'string',
                                'example': 'The updated content of the sales report.'
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
                                'example': {'title': 'This field is required.'}
                            }
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Report not found.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'error': {
                                'type': 'string',
                                'example': 'Report not found.'
                            }
                        }
                    }
                }
            }
        }
    }
})
def update_report(id):
    data = request.get_json()
    errors = report_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    report = Report.query.get(id)  # Find the report by ID
    if not report:
        return jsonify({"error": "Report not found"}), 404

    # Update the report with the new data (replace the entire resource)
    for key, value in data.items():
        setattr(report, key, value)

    db.session.commit()  # Commit the changes to the database
    
    return jsonify(report_schema.dump(report)), 200