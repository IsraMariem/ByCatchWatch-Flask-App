from flask import Flask
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






















"""from flask import Flask
from app.extensions import db, ma, migrate
from app.routes import ports, bycatch, species, report
import os
from app.routes.visualizations import visualization_bp
from app.routes.clustering import clustering_bp
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.routes.auth import auth_bp

bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    app.config['SESSION_COOKIE_SECURE'] = False  # Only in development, not for production!
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Or 'Strict' depending on your needs
    app.config['SECRET_KEY'] = 'ISRA147'
    app.config['DEBUG'] = True

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    # Register blueprints
    app.register_blueprint(ports.bp)
    app.register_blueprint(bycatch.bp)
    app.register_blueprint(species.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(visualization_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(clustering_bp)

    return app

"""

    

    
    

