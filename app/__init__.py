# This module initialises our application, doing all configurations
# it returns an app instance,
# and here is also where we create a database instance.

# we start by importing Flask from flask, which will be used to create an app instance.
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# for configuring the app we will need the DevConfig from our config.py module therefore we import this aswell.
# from flask_user import UserManager

from app.config import DevConfig
# we will also need to do some initialisation (configuration) to our forms module ??????? where
# (which is inside app >> main >> forms.py)



db = SQLAlchemy()
login = LoginManager()
mail = Mail()

# we start by creating a database instance which we will use in our models.py for creating the database.
from app.populate import populate_db

# we then initialise the application:
# config_class ->> under this variable we need to input the DevConfig
#                  we made in our configuration file.
def create_app(config_class=DevConfig):
    # we start by creating an instance of an app.
    app = Flask(__name__)
    # these just configure flask mail and ensure it always sends from our new email
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'space4less54@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Space4Less'
    # mail = Mail(app)
    mail.init_app(app)

    # configuring (initialising and stuff):
    app.config.from_object(config_class)

    # this links the db to the app
    db.init_app(app)
    # initialising the login function
    login.init_app(app)
    login.login_view = 'login'
    login.login_message_category = 'info'

    # for demonstration purposes:
    # from app.populate import populate_db
    from app.models import User, Post
    # user_manager = UserManager(app, db, User)
    # creating columns and populating database
    with app.app_context():
        db.create_all()  # creates table structure for each imported user
        populate_db()  # adding dummy data

    # somehow i need to initialise the UserManager (which needs 3 inputs- app, db and User

    from app.main.routes import bp_main
    from app.booking.routes import bp_booking
    from app.auth.routes import bp_auth
    from app.posts.routes import bp_posts
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_booking)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_posts)

    return app
