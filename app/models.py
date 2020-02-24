
from sqlalchemy import Column, ForeignKey, Integer, String
# importing databse instance from __init__ of app
from app import db
# importing for encryption purposes
from werkzeug.security import generate_password_hash, check_password_hash

# # Define the classes and tables

# # Columns for user table: user_id (INTEGER PRIMARY KEY), username (TEXT NOT NULL), email (TEXT NOT NULL)

class User(db.Model):
    __tablename__ = 'registered_user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(200))
    role = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s')>" % (self.user_id, self.username, self.email, self.role)

    # for the password to be enctipted:
    # for generating
    def set_password(self, password):
        self.password = generate_password_hash(password)
    # for reading password

    def check_password(self, password):
        return check_password_hash(self.password, password)


