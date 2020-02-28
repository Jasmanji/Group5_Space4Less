# importing databse instance from __init__ of app
from sqlalchemy import Column, ForeignKey, Integer, String
from app import db
# importing for encryption purposes
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import login


# # Define the classes and tables
# # userMixin is a provided class from flask documentation to assist log in functionality
# # Columns for user table: user_id (INTEGER PRIMARY KEY), username (TEXT NOT NULL), email (TEXT NOT NULL)

class User( db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(200))
    role = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.username, self.email, self.image_file)

    # for the password to be encrypted:
    # for generating
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # for reading password

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    content = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.title, self.date_posted, self.image)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
