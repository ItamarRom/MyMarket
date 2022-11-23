# Importing the db object created in __init__.py
from app import db
from datetime import datetime
# handling password hashing
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# Importing the login object created in __init__.py
# Will be used to implement a user loader
from app import login
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# These classes inherit from db.Model which is a base class for all models
# Creating these classes is how we define the table and its columns inside our DB
# The UserMixin class inheritance provides generic login implementations for a standard user class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String())
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    items = db.relationship('Item', backref='owner', lazy='dynamic')
    last_seen = db.Column(db.DateTime,nullable=True, default=datetime.utcnow())

    def __repr__(self):
        return f'<User {self.username}>'

    # Responsible for the password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Responsible for verifying the hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=robohash&s={size}'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='c_item', lazy='dynamic')

    def __repr__(self):
        return f'<item {self.name}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __repr__(self):
        return f'<Comment: {self.body}'
