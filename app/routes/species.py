from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Species
from app.schemas import SpeciesSchema

bp = Blueprint('species', __name__, url_prefix='/species')

# Instantiate schema
species_schema = SpeciesSchema()
speciess_schema = SpeciesSchema(many=True)

# Create a new species
@bp.route('/', methods=['POST'])
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
def get_species():
    species = Species.query.all()  # fetch all species from the database
    return jsonify(species_schema.dump(species,many=True)), 200  # use .dump() to serialize the data