from flask import Blueprint, jsonify, request, abort
from .models import User, db
from .utils import is_valid_email
import bcrypt

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
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
        }
        user_list.append(user_data)

    return jsonify(users=user_list), 200

@main_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Extract the required information from the request data
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Perform validation checks on the data
    if not username or not email or not password:
        abort(400, "Username, email, and password are required.")

    if len(username) < 3 or len(username) > 20:
        abort(400, "Username must be between 3 and 20 characters.")

    if not is_valid_email(email):
        abort(400, "Invalid email address.")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    # Create a new User instance
    new_user = User(username=username, email=email, password=hashed_password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    status_code = 200
    response_data = {
        "message": "User created successfully",
        "user_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

    return jsonify(response_data), status_code  
