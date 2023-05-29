import os
from dotenv import load_dotenv

load_dotenv('.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Additional development-specific configuration options
    # Development database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    
class ProductionConfig(Config):
    DEBUG = False
    # Additional production-specific configuration options

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    # Add more configuration options if needed
}