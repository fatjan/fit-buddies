import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = False
    # Add more configuration options here

class DevelopmentConfig(Config):
    DEBUG = True
    # Additional development-specific configuration options

class ProductionConfig(Config):
    DEBUG = False
    # Additional production-specific configuration options
