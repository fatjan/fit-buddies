from flask import Blueprint, jsonify, request, abort
from .models import User, db, Workout
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
    if user and User.check_password(password, user['password']):
        token = User.generate_token(user['id'])
        return jsonify({'message': 'Login successful', "token": token}), 200

    return jsonify({'message': 'Invalid username or password'}), 401

@main_bp.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    # Get the data from the request body
    data = request.get_json()

    # Retrieve the user from the database based on the user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'})

    # Update the user attributes if provided in the request data
    if 'username' in data:
        user.username = data['username']

    if 'email' in data:
        if not is_valid_email(data['email']):
            abort(400, "Invalid email address.")
        user.email = data['email']

    if 'name' in data:
        user.name = data['name']

    # Save the changes to the database
    db.session.commit()

    # Return a response indicating the successful update
    return jsonify({'message': 'User updated successfully'}), 200

@main_bp.route('/workout', methods=['POST'])
def create_workout():
    data = request.get_json()
    name = data.get('name')
    duration = data.get('duration')
    intensity = data.get('intensity')
    calories_burned = data.get('calories_burned')
    user_id = request.headers.get('user_id')

    if not name or not duration or not intensity or not calories_burned:
        return jsonify({'message': 'Missing required fields'}), 400

    workout = Workout(name=name, duration=duration, intensity=intensity, calories_burned=calories_burned, user_id=user_id)

    db.session.add(workout)
    db.session.commit()

    return jsonify({'message': 'Workout created successfully'}), 201

@main_bp.route('/workouts', methods=['GET'])
def get_workouts():
    user_id = request.headers.get('user_id')
    print(user_id)
    if not user_id:
        return jsonify({'message': 'Missing user_id in headers'}), 400

    workouts = Workout.query.filter_by(user_id=user_id).all()

    workout_data = []
    for workout in workouts:
        workout_data.append({
            'id': workout.id,
            'name': workout.name,
            'duration': workout.duration,
            'intensity': workout.intensity,
            'calories_burned': workout.calories_burned,
            'created_at': workout.created_at
        })

    return jsonify({'workouts': workout_data}), 200