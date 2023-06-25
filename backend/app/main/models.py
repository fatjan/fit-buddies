from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

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
