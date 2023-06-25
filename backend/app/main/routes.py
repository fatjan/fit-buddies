from flask import Blueprint, jsonify, request, abort
from .models import User, db, Workout
from .utils import is_valid_email
import bcrypt
from dotenv import load_dotenv
import os
import requests

load_dotenv('../../.env')

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
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authorization header is missing'}), 401

    if not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Invalid authorization header'}), 401

    token = auth_header.split(' ')[1]
   
    # Retrieve the user ID from the token
    user_id = User.get_user_id_from_token(token)
    if not user_id:
        return jsonify({'message': 'Invalid or expired token'}), 401
    
    data = request.get_json()
    name = data.get('name')
    duration = data.get('duration')
    intensity = data.get('intensity')
    calories_burned = data.get('calories_burned')

    if not name or not duration or not intensity or not calories_burned:
        return jsonify({'message': 'Missing required fields'}), 400

    workout = Workout(name=name, duration=duration, intensity=intensity, calories_burned=calories_burned, user_id=user_id)

    db.session.add(workout)
    db.session.commit()

    return jsonify({'message': 'Workout created successfully'}), 201

@main_bp.route('/workouts', methods=['GET'])
def get_workouts():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authorization header is missing'}), 401

    if not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Invalid authorization header'}), 401

    token = auth_header.split(' ')[1]
    
    # Retrieve the user ID from the token
    user_id = User.get_user_id_from_token(token)
    if not user_id:
        return jsonify({'message': 'Invalid or expired token'}), 401

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

@main_bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    api_key = os.environ.get('WEATHER_API_KEY')

    # API endpoint URL
    url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={api_key}"

    try:
        # Send GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        # Parse the JSON response
        data = response.json()

        # Extract relevant information from the response
        result = {
            'location': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country'],
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'feels_like': data['current']['feelslike_c'],
            'time': data['location']['localtime'],
            'uv': data['current']['uv'],
        }
        return result
    except requests.exceptions.HTTPError as err:
        return f"HTTP Error occurred: {err}"
    except requests.exceptions.RequestException as err:
        return f"Request Exception occurred: {err}"

@main_bp.route('/forecast', methods=['GET'])
def get_forecaset_weather():
    city = request.args.get('city')
    api_key = os.environ.get('WEATHER_API_KEY')

    # API endpoint URL
    url = f"https://api.weatherapi.com/v1/forecast.json?q={city}&key={api_key}"

    days = request.args.get('days')
    if days:
        url += f"&days={days}"
    
    hour = request.args.get('hour')
    if hour:
        url += f"&hour={hour}"

    try:
        # Send GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        # Parse the JSON response
        data = response.json()

        if 'forecastday' in data['forecast']:
            forecast = data['forecast']['forecastday']
            forecast_data = []
            for i in range(len(forecast)):
                item = forecast[i]
                day = {
                    'date': item['date'],
                    'max_temp': item['day']['maxtemp_c'],
                    'min_temp': item['day']['mintemp_c'],
                    'condition': item['day']['condition']['text'],
                    'uv': item['day']['uv'],
                    'daily_chance_of_rain': item['day']['daily_chance_of_rain'],
                    'daily_will_it_rain': item['day']['daily_will_it_rain'],
                }
                hour = {
                    'time': item['hour'][0]['time'],
                    'temp_c': item['hour'][0]['temp_c'],
                    'condition': item['hour'][0]['condition']['text'],
                    'chance_of_rain': item['hour'][0]['chance_of_rain'],
                    'will_it_rain': item['hour'][0]['will_it_rain'],
                    'feels_like': item['hour'][0]['feelslike_c'],
                    'uv': item['hour'][0]['uv'],
                }
                forecast_data.append({
                    'day': day,
                    'hour': hour
                })

        # Extract relevant information from the response
        result = {
            'location': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country'],
            'current': {
                'temperature': data['current']['temp_c'],
                'condition': data['current']['condition']['text'],
                'feels_like': data['current']['feelslike_c'],
                'time': data['location']['localtime'],
                'uv': data['current']['uv'],
            },
            'forecast': forecast_data
        }
        return result
    except requests.exceptions.HTTPError as err:
        return f"HTTP Error occurred: {err}"
    except requests.exceptions.RequestException as err:
        return f"Request Exception occurred: {err}"