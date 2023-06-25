from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
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
        print(login_password, password_hash)
        return bcrypt.checkpw(login_password.encode('utf-8'), bytes.fromhex(password_hash[2:]))

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return {
            "id": self.id,
            "name": self.username,
            "duration": self.name,
            "intensity": self.intensity,
            "calories_burned": self.calories_burned,
            "created_at": self.created_at
        }
