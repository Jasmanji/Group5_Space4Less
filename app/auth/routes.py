from flask import url_for, flash, redirect, render_template, request, Blueprint
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from wtforms import ValidationError

from app import db, mail
from app.auth.forms import LoginForm, EmailForm, PasswordReset, RegistrationForm
from app.models import User

# we create an instance of blueprint as main
bp_auth = Blueprint('auth', __name__)


# route for the signup:
# lines before form instance are a way to ensure if a user is ALREADY logged in
# they will just be redirected back to the home page if they attempt to go to this route.
# If the user sends a POST request of the RegistrationForm(),
# We query all users to check there's not such email or username already taken.
# Otherwise, if the email and username don't exist, we create a user row in the database,
# with all the form details the user entered. We also create the user's password by running the
# function that hashes it.
# We then add this user to the database and commit the session.
# We then return the user to the login page where they are now able to log in.
@bp_auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form_signup = RegistrationForm()
    if form_signup.validate_on_submit():  # this will tell us if the for was valid when submitted
        user_username = User.query.filter_by(username=form_signup.username.data).first()
        user_email = User.query.filter_by(username=form_signup.email.data).first()
        if user_username or user_email is not None:
            raise ValidationError('This username is already taken! please choose another username', 'danger')
        else:
            user = User(username=form_signup.username.data,
                        first_name=form_signup.firstname.data,
                        last_name=form_signup.surname.data,
                        email=form_signup.email.data,
                        roles=form_signup.role.data)
            user.set_password(form_signup.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you have created an account! Please log in to continue browsing!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('signup.html', title='signup', form=form_signup)


# route for the login
# lines before form instance are a way to ensure if a user is ALREADY logged in
# they will just be redirected back to the home page.
# the user query is where they are actually logged in, and the first() is used
# bc we just want one result (for the username) and then when the username is identified
# the check password checks the password input against that which exists in the database
# associated with that username
# the final section is where there are no errors and the user is officially logged in
# using the log in function
@bp_auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

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
                return redirect(url_for('auth.login'))
            else:
                login_user(user, remember=form_login.remember.data)
                flash('Login successful!', 'success')
                next_page = request.args.get(
                    'next')  # will get the page the user wanted to go to before they were redirected to login
                return redirect(next_page) if next_page else redirect(url_for(
                    'main.home_page'))  # will redirect user to the page they requested before they tried to log in,
                # otherwise they will be redirected to home.
    return render_template('login.html', title='Login Page', form=form_login)


@bp_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home_page'))


def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset',
                  sender='space4less54@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Click the following link to reset your password.
    {url_for('auth.reset_password', token=token, _external=True)}
    '''
    mail.send(msg)


@bp_auth.route('/reset', methods=['GET', 'POST'])
def reset_email():
    form_reset = EmailForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form_reset.email.data).first()
        if user is None:
            flash('This email is not associated with an account')

        else:
            send_email(user)
            flash('Email has been sent!')
        return render_template('email_password_reset.html', form=form_reset)

    return render_template('email_password_reset.html', form=form_reset)


@bp_auth.route('/update_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    form_password = PasswordReset()
    if form_password.validate_on_submit():
        hashed_password = generate_password_hash(form_password.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('password has been updated', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('actual_password_reset.html', form=form_password)
