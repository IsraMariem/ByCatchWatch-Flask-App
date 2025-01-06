from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Report
from app.schemas import ReportSchema

bp = Blueprint('reports', __name__, url_prefix='/reports')

# Instantiate schema
report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)

# Create a new report
@bp.route('/', methods=['POST'])
def create_report():
    data = request.get_json()
    errors = report_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    new_report = Report(**data)
    db.session.add(new_report)
    db.session.commit()

    return jsonify(report_schema.dump(new_report)), 201  # Use dump() to serialize the new report


# Get all reports
@bp.route('/', methods=['GET'])
def get_reports():
    reports = Report.query.all()  # Fetch all reports from the database
    return jsonify(reports_schema.dump(reports, many=True)), 200  # Use dump() to serialize the data as a list

