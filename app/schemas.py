# Marshmallow schemas

from marshmallow import Schema, fields, validate
from app.models import Port, Bycatch, Species, Report

# Port Schema
class PortSchema(Schema):
    port_id = fields.Str(required=True)   
    name = fields.Str(required=True, validate=validate.Length(min=1))
    size = fields.Str(required=True, validate=validate.OneOf(["Small", "Medium", "Large"]))
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    authority_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()

# Bycatch Stat Schema
class BycatchStatSchema(Schema):
    bycatch_id = fields.Str(required=True)   
    gear_type = fields.Str(required=True)
    bpue = fields.Float(required=True)
    total_catch = fields.Int(required=True)
    port_id = fields.Str(required=True)
    species_id = fields.Str(required=True)
    quantity = fields.Int(required=True)
    total_catch = fields.Int()
    date_caught = fields.Date(nullable=False)

# Species Schema
class SpeciesSchema(Schema):
    species_id = fields.Str(required=True)  
    scientific_name = fields.Str(required=True)
    common_name = fields.Str()
    iucn_status = fields.Str(required=True)
    estimated_catch = fields.Int(required=True)
    mortality_rate = fields.Float(required=True)
    origin = fields.Str(validate=validate.OneOf(["Native","Migratory","Invasive"]))


# Report Schema
class ReportSchema(Schema):
    report_id = fields.Str(required=True)  
    species_id = fields.Str(required=True)
    bycatch_id = fields.Str(required=True)
    reporter_name = fields.Str(required=True)
    gear_type = fields.Str(required=True)
    contact_info = fields.Str(required=True)
    remarks = fields.Str()
    quantity = fields.Int(required=True)
    date = fields.Date(format='%Y-%m-%d', required=True)
