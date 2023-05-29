import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Additional development-specific configuration options
    # Development database configuration
    DATABASE_URI = 'postgresql://fatma.storage:4OweuG2zVRAf@ep-shrill-darkness-863214.ap-southeast-1.aws.neon.tech/neondb'

    @property
    def DATABASE_HOST(self):
        return self.DATABASE_URI.split('@')[1].split('/')[0]

    @property
    def DATABASE_NAME(self):
        return self.DATABASE_URI.split('/')[-1]

    @property
    def DATABASE_USER(self):
        return self.DATABASE_URI.split('//')[1].split(':')[0]

    @property
    def DATABASE_PASSWORD(self):
        return self.DATABASE_URI.split('//')[1].split(':')[1].split('@')[0]

    @property
    def DATABASE_PORT(self):
        return '5432'  # Assuming the default PostgreSQL port

class ProductionConfig(Config):
    DEBUG = False
    # Additional production-specific configuration options

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    # Add more configuration options if needed
}