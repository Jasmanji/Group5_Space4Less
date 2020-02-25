# the render template is to help us with returning an html template for a route
# the url_for is a function within flask that will find the exact location of routes for us
from flask import render_template, url_for, redirect, flash, Blueprint, request

from sqlalchemy.exc import IntegrityError

from app import RegistrationForm, db
# we also need to import the forms
from app.main.forms import LoginForm
from app.models import User

# we create an instance of blueprint as main
bp_main = Blueprint('main', __name__)


# route for home page.
@bp_main.route('/')
@bp_main.route('/home')
def home_page():
    return render_template('home.html', title='Home Page')


@bp_main.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method=='POST':  # this will tell us if the for was valid when submitted
        user = User(username=form.username.data, first_name=form.firstname.data, last_name=form.surname.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('congratulations, you have created an account!', 'success')
            return redirect(url_for('main.home_page'))
        except IntegrityError:
            db.session.rollback()
            flash('there was something wrong with your password or email!', 'error')
    return render_template('signup.html', title='signup', form=form)


# route for the login
@bp_main.route("/login", methods=['GET', 'POST'])
def login():
    form_instance = LoginForm()
    return render_template('login.html', title='Login Page', form=form_instance)

@bp_main.route("/account")
def account():
    return render_template('account.html', title='account' , username='Aure')

@bp_main.route("/notifications")
def notifications():
    return render_template('notifications.html', title='Notifications')