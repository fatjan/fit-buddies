from app import create_app
from dotenv import load_dotenv

load_dotenv('.env')

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    # Run the app
    app.run()
