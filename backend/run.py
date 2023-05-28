import os
from app import create_app

# Get the environment name, defaulting to 'development'
env = os.environ.get('FLASK_ENV', 'development')

# Create the Flask app
app = create_app(env)

if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
