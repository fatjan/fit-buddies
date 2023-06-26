from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import jwt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "gender": self.gender,
            "weight": self.weight,
            "created_at": self.created_at
        }

    @staticmethod
    def get_users():
        users = User.query.all()

        users_list = []
        for user in users:
            user_dict = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.name,
                'password': user.password,
                'created_at': user.created_at
            }
            users_list.append(user_dict)

        return users_list

    def get_user_by_username(username):
        user = User.query.filter_by(username=username).first_or_404()

        user_dict = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'password': user.password,
            'created_at': user.created_at
        }

        return user_dict

    @staticmethod
    def check_password(login_password, password_hash):
        return bcrypt.checkpw(login_password.encode('utf-8'), bytes.fromhex(password_hash[2:]))

    @staticmethod
    def generate_token(user_id):
        # Set the expiration time for the token (e.g., 1 day from the current time)
        expiration = datetime.utcnow() + timedelta(days=1)

        # Create the payload containing user information and expiration time
        payload = {'user_id': user_id, 'exp': expiration}

        # Generate the JWT token using a secret key
        token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')

        return token

    @staticmethod
    def get_user_id_from_token(token):
        try:
            decoded_token = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            user_id = decoded_token['user_id']
            return user_id
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except jwt.InvalidTokenError:
            # Handle invalid token
            return None

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('workouts', lazy=True))

    def __repr__(self):
        return {
            "id": self.id,
            "name": self.username,
            "duration": self.name,
            "intensity": self.intensity,
            "calories_burned": self.calories_burned,
            "created_at": self.created_at,
            "user_id": self.user_id
        }
