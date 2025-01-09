from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Report
from app.schemas import ReportSchema

bp = Blueprint('reports', __name__, url_prefix='/reports')


report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)

from flask_login import login_required

# Add new report
@bp.route('/', methods=['POST'])
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
def get_reports():
    reports = Report.query.all()  
    return jsonify(reports_schema.dump(reports, many=True)), 200 

