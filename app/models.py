from datetime import datetime
from app.extensions import db
from enum import Enum, auto


class Port(db.Model):
    __tablename__ = 'ports'
    port_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    size = db.Column(db.String(50), nullable=False)  # Small, Medium, Large
    region = db.Column(db.String(100), nullable=True)  
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    authority_name = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))



    bycatch = db.relationship('Bycatch', backref='port', lazy=True)

class Species(db.Model):
    __tablename__ = 'species'
    species_id = db.Column(db.String, primary_key=True)
    scientific_name = db.Column(db.String(100), nullable=False)
    common_name = db.Column(db.String(100)) 
    iucn_status = db.Column(db.String(50), nullable=False)
    estimated_catch = db.Column(db.Integer, nullable=False)
    mortality_rate = db.Column(db.Float, nullable=False)
    origin = db.Column(db.String(50)) 

    bycatch = db.relationship('Bycatch', backref='species', lazy=True)

class Bycatch(db.Model):
    __tablename__ = 'bycatch'
    bycatch_id = db.Column(db.String, primary_key=True)
    port_id = db.Column(db.String, db.ForeignKey('ports.port_id'), nullable=False)
    species_id = db.Column(db.String, db.ForeignKey('species.species_id'), nullable=False)
    date_caught = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    gear_type = db.Column(db.String,nullable=False)    
    bpue = db.Column(db.Float,nullable=False) 
    total_catch = db.Column(db.Integer ,nullable=True)

    report = db.relationship('Report', backref='bycatch', uselist=False)

class Report(db.Model):
    __tablename__ = 'reports'
    report_id = db.Column(db.String, primary_key=True)
    bycatch_id = db.Column(db.String, db.ForeignKey('bycatch.bycatch_id'), nullable=False)
    species_id = db.Column(db.String,db.ForeignKey('species.species_id'),nullable=False)
    reporter_name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    gear_type = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date,nullable=False)

    species = db.relationship('Species', backref='reports', uselist=False)


from app.extensions import db
from flask_login import UserMixin


class UserBackground(Enum):
    RESEARCHER = 'Researcher'
    FISHERMAN = 'Fisherman'
    NGO = 'NGO'
    BYCATCH_ACTIVIST = 'Bycatch Activist'
    OBSERVER = 'Observer'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    background = db.Column(db.Enum(UserBackground), nullable=False) 
    def __repr__(self):
        return f"<User {self.username}>"

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)