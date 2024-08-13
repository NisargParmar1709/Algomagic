from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<User {self.email}>"

class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    logout_time = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)
    
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
