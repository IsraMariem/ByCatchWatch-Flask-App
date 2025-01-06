
from flask import Flask
from app.extensions import db, ma, migrate
from app.routes import ports, bycatch, species, report
import os
from .visualizations import visualization_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(ports.bp)
    app.register_blueprint(bycatch.bp)
    app.register_blueprint(species.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(visualization_bp)


    # Create tables if they don't exist (you can add this after initializing the app)
    with app.app_context():
        db.create_all()  # Creates all tables defined in your SQLAlchemy models
    
    return app