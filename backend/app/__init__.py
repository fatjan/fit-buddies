from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .main.routes import main_bp
from config import config
from app.main.models import db
import os


def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # Configure app settings
    app.config["SECRET_KEY"] = "your_secret_key_here"
    env = os.environ.get('FLASK_ENV', 'development')

    app.config.from_object(config[env])
    
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(main_bp)

    return app
