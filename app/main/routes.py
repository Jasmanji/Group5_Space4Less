# the render template is to help us with returning an html template for a route
# the url_for is a function within flask that will find the exact location of routes for us
from flask import render_template, url_for, redirect, flash, Blueprint, request

from app import RegistrationForm, db
# we also need to import the forms
from app.main.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required

# we create an instance of blueprint as main
bp_main = Blueprint('main', __name__)

# bp_auth = Blueprint('auth', __name__)

# route for home page.
@bp_main.route('/')
@bp_main.route('/home')
def home_page():
    return render_template('home.html', title='Home Page')


@bp_main.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form_signup = RegistrationForm()
    if form_signup.validate_on_submit():  # this will tell us if the for was valid when
        # submitted
        user = User(username=form_signup.username.data, role=form_signup.role.data,
                    first_name=form_signup.firstname.data, last_name=form_signup.surname.data,
                    email=form_signup.email.data)
        user.set_password(form_signup.password.data)
        db.session.add(user)
        db.session.commit()
        flash('congratulations, you have created an account!', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('signup.html', title='signup', form=form_signup)


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
        return redirect(url_for('main.home_page'))
    # if current_user.is_authenticated:
    #   return redirect(url_for('home_page'))
    # we create an instance of the form the user inputted
    form_login = LoginForm()

    # we want to check that the form submitted by the username exists, so we can check the email address exists: to
    # do this, we query to see if there's any value in the column email which matches to the email the user inputted
    # in the form. first else statement = correct login details, the second else statement is where the query returns
    # no users matching that email

    if form_login.validate_on_submit():
        if form_login.validate_on_submit():
            user = User.query.filter_by(email=form_login.email.data).first()
            if user is None or not user.check_password(form_login.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            else:
                login_user(user, remember=form_login.remember.data)
                flash('Login successful!', 'success')
                next_page=request.args.get('next') # will get the page the user wanted to go to before they were redirected to login
                return redirect(next_page) if next_page else redirect(url_for('main.home_page')) # will redirect user to the page they requested before they tried to log in, otherwise they will be redirected to home.
    return render_template('login.html', title='Login Page', form=form_login)


@bp_main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home_page'))


@bp_main.route("/account")
@login_required
def account():
    return render_template('account.html', title='account')


@bp_main.route("/notifications")
@login_required
def notifications():
    return render_template('notifications.html', title='Notifications')
