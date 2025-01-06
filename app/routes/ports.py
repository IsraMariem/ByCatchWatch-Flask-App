from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Port
from app.schemas import PortSchema

bp = Blueprint('ports', __name__, url_prefix='/ports')

# Instantiate schema
port_schema = PortSchema()
ports_schema = PortSchema(many=True)

# Create a new port
@bp.route('/', methods=['POST'])
def create_port():
    # Validate input data
    data = request.get_json()
    errors = port_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Create new Port
    new_port = Port(**data)
    db.session.add(new_port)
    db.session.commit()
    
    return port_schema.jsonify(new_port), 201

# Get all ports
@bp.route('/', methods=['GET'])
def get_ports():
    # Query all ports from the database
    ports = Port.query.all()

    # Serialize the data using the schema
    ports_data = ports_schema.dump(ports)  # Use dump() to serialize the data

    # Return the serialized data as a JSON response
    return jsonify(ports_data), 200

