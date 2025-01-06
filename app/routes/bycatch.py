from flask import Blueprint, request, jsonify
from app.extensions import db

from flask_login import login_required
bp = Blueprint('bycatch', __name__, url_prefix='/bycatch')




from app.schemas import BycatchStatSchema

bycatch_schema = BycatchStatSchema()
bycatchs_schema = BycatchStatSchema(many=True)

from app.models import Bycatch

# Create a new Bycatch
@bp.route('/', methods=['POST'])
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
def get_bycatch():
    bycatch = Bycatch.query.all()  
    return jsonify(bycatch_schema.dump(bycatch, many=True)), 200  
