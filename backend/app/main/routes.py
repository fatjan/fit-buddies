from flask import Blueprint, jsonify, request
from .models import User, db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return jsonify(message="Welcome to the main endpoint")

@main_bp.route("/users")
def get_users():
    users = User.query.all()
    user_list = []

    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email
            # Add more fields as needed
        }
        user_list.append(user_data)

    return jsonify(users=user_list)

@main_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Extract the required information from the request data
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Perform validation checks on the data if needed

    # Create a new User instance
    new_user = User(username=username, email=email, password=password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Return a success message or any other desired response
    return jsonify(message="User registered successfully")
