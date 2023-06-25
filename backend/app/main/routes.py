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
            "name": user.name,
            "created_at": user.created_at,
        }
        user_list.append(user_data)

    return jsonify(users=user_list), 200

@main_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Extract the required information from the request data
    username = data.get("username")
    name = data.get("name")
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
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create a new User instance
    new_user = User(username=username, email=email, password=hashed_password, name=name)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    status_code = 200
    response_data = {
        "message": "User created successfully",
        "user_id": new_user.id,
        "username": new_user.username,
        "name": new_user.name,
        "email": new_user.email,
        "created_at": new_user.created_at,
    }

    return jsonify(response_data), status_code  


@main_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.get_user_by_username(username)
    print('user', user)
    if user and User.check_password(password, user['password']):
        return jsonify({'message': 'Login successful'})

    return jsonify({'message': 'Invalid username or password'}), 401

# from flask import jsonify, request
# from .controller.user import get_users, signup
# from app.main import main_bp

# @main_bp.route("/")
# def index():
#     return jsonify(message="Welcome to the main endpoint")

# @main_bp.route("/users",  methods=["GET"])
# def get_users_route():
#     users = get_users()
#     return jsonify(users=users), 200

# @main_bp.route("/signup", methods=["POST"])
# def signup_route():
#     data = request.get_json()
#     response_data = signup(data)
#     return jsonify(response_data), 200
