from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .main.routes import main_bp

def create_app(env=None):
    # Create the Flask app
    app = Flask(__name__)

    # Configure app settings
    app.config["SECRET_KEY"] = "your_secret_key_here"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://fatma.storage:4OweuG2zVRAf@ep-shrill-darkness-863214.ap-southeast-1.aws.neon.tech/neondb"
    app.config.from_object(config[env])
    
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(main_bp)

    return app
