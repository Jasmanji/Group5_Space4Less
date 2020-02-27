# the render template is to help us with returning an html template for a route
# the url_for is a function within flask that will find the exact location of routes for us
from flask import render_template, url_for, redirect, flash, Blueprint, request

from app import RegistrationForm, db
# we also need to import the forms
from app.main.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user
# we create an instance of blueprint as main
bp_main = Blueprint('main', __name__)
#bp_auth = Blueprint('auth', __name__)


# route for home page.
@bp_main.route('/')
@bp_main.route('/home')
def home_page():
    return render_template('home.html', title='Home Page')


@bp_main.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':  # this will tell us if the for was valid when submitted
        user = User(username=form.username.data, role=form.role.data, first_name=form.firstname.data,
                    last_name=form.surname.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('congratulations, you have created an account!', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('signup.html', title='signup', form=form)


# route for the login
# lines before form instance are a way to ensure if a user is ALREADY logged in
# they will just be redirected back to the home page
# the user query is where they are actually logged in, and the first() is used
# bc we just want one result (for the username) and then when the username is identified
# the check password checks the password input against that which exists in the database
# associated with that username
# the final section is where there are no errors and the user is officially logged in
# using the log in function
@bp_main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form_instance = LoginForm()
    if form_instance.validate_on_submit():
        user = User.query.filter_by(username=form_instance.username.data).first()
        if user is None or not user.check_password(form_instance.password.data):
            flash('Invalid Login')
            return redirect(url_for('login'))
        login_user(user, remember=form_instance.remember_me.data)
        flash('congrats you are logged in {}' .format(user.username))
        return redirect(url_for('home_page'))
    return render_template('login.html', title='Login Page', form=form_instance)


@bp_main.route("/account")
def account():
    return render_template('account.html', title='account', username='Aure')


@bp_main.route("/notifications")
def notifications():
    return render_template('notifications.html', title='Notifications')
