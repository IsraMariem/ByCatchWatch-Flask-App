from flask import Flask
from app.extensions import db, ma, migrate, bcrypt, login_manager
from app.routes import ports, bycatch, species, report
import os
from app.routes.visualizations import visualization_bp
from app.routes.auth import auth_bp
from app.models import User  
from app.routes.recomm import bp_recom
from app.routes.clustering import clustering_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Add user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # This function fetches the user by ID

    # Register blueprints
    app.register_blueprint(ports.bp)
    app.register_blueprint(bycatch.bp)
    app.register_blueprint(species.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(visualization_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bp_recom, url_prefix='/api')
    app.register_blueprint(clustering_bp, url_prefix='/clustering')
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app





















"""from flask import Flask
from app.extensions import db, ma, migrate
from app.routes import ports, bycatch, species, report
import os
from app.routes.visualizations import visualization_bp
from app.routes.clustering import clustering_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    app.config['DEBUG'] = True

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
    app.register_blueprint(clustering_bp)
    
    return app

"""









