# the render template is to help us with returning an html template for a route
# the url_for is a function within flask that will find the exact location of routes for us
from flask import render_template, url_for, redirect, flash, Blueprint, request, app, current_app
import os
import secrets
from app import db
from PIL import Image
# we also need to import the forms
from app.main.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from app.models import User, Post, Book
from flask_login import current_user, login_user, logout_user, login_required

# we create an instance of blueprint as main
bp_main = Blueprint('main', __name__)


# def role_required(required_role):
#     def has_role(current_user):
#         return current_user.roles == required_role
#
#     def role_decorator(func):
#         def function_wrapper(*args, **kwargs):
#             if has_role(current_user):
#                 func(*args, **kwargs)
#             else:
#                 raise Exception(f'not allowed :(. requires role <<{required_role}>>')
#
#         return function_wrapper
#
#     return role_decorator
#


# route for home page.
@bp_main.route('/')
@bp_main.route('/home')
def home_page():
    posts = Post.query.all()
    return render_template('home.html', title='Home Page', posts=posts)


# bp_main.route("/search", methods=['POST'])
# def search():
#    query = request.args('search')
#   return render_template('search.html', title='Search', search=search)

@bp_main.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        term = request.form['search_term']
        if term == "":
            flash("Enter a location/size to search for")
            return redirect('/')
        results = Post.query.filter(Post.location.contains(term)).all()
        if not results:
            flash("No post found matching this data.")
            return redirect('/')
        return render_template('search.html', results=results)
    else:
        return redirect(url_for('main.home_page'))


@bp_main.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form_signup = RegistrationForm()
    if form_signup.validate_on_submit():  # this will tell us if the for was valid when
        # submitted
        user = User(username=form_signup.username.data,
                    first_name=form_signup.firstname.data,
                    last_name=form_signup.surname.data,
                    email=form_signup.email.data,
                    roles=form_signup.role.data)
        user.set_password(form_signup.password.data)
        # adding the role of the user- property_owner or renter

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
                return redirect(url_for('main.login'))
            else:
                login_user(user, remember=form_login.remember.data)
                flash('Login successful!', 'success')
                next_page = request.args.get(
                    'next')  # will get the page the user wanted to go to before they were redirected to login
                return redirect(next_page) if next_page else redirect(url_for(
                    'main.home_page'))  # will redirect user to the page they requested before they tried to log in,
                # otherwise they will be redirected to home.
    return render_template('login.html', title='Login Page', form=form_login)


@bp_main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home_page'))


def saving_pictures_post(post_picture):
    hide_name = secrets.token_hex(6)
    _, f_extension = os.path.splitext(post_picture.filename)
    post_image = hide_name + f_extension
    config = current_app.config
    post_path = os.path.join(config['POST_UPLOAD'], post_image)
    output_size = (100, 100)
    final = Image.open(post_picture)
    final.thumbnail(output_size)
    final.save(post_path)
    return post_image


@bp_main.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form_post = PostForm()
    if form_post.validate_on_submit():
        if form_post.picture_for_posts.data:
            file = request.files['picture_for_posts']

            pic = saving_pictures_post(file)
            form_post.picture_for_posts = pic
            post = Post(title=form_post.title.data, content=form_post.content.data,
                        image=form_post.picture_for_posts, location=form_post.location.data,
                        space_size=form_post.space_size.data,
                        author=current_user)
            db.session.add(post)
            db.session.commit()
        flash('you have successfully posted your property!!', 'success')
        return redirect(url_for('main.home_page'))
    image = url_for('static', filename='post_pictures/' + str(form_post.picture_for_posts))
    return render_template('post.html', title='Post', content='content', image=image, form=form_post)


@bp_main.route('/book/<postid>')
@login_required
def book(postid):
    book = Book(user_id=current_user.get_id() , post_id=postid)
    db.session.add(book)
    db.session.commit()
    flash('you have successfully posted a request for the property')
    bookings= Book.query.join(User)
    return render_template('home.html')

@bp_main.route('/bookings')
@login_required
def bookings():
    user = current_user.get_id()
    print(user)
    bookings = Book.query.join(Post, Book.post_id == Post.post_id).join(User, User.user_id == Book.user_id).filter_by(user_id=user).all()
    
    print(bookings)
    return render_template('bookings.html', title='Book', bookings=bookings)

def saving_pictures(profile_picture):
    hide_name = secrets.token_hex(6)
    _, f_extension = os.path.splitext(profile_picture.filename)
    p_pic = hide_name + f_extension
    pic_path = os.path.join(current_app.config['UPLOAD_FOLDER'], p_pic)
    profile_picture.save(pic_path)
    return p_pic



@bp_main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form_account = UpdateAccountForm()
    if form_account.validate_on_submit():
        if form_account.picture.data:
            file = request.files['picture']
            pic = saving_pictures(file)
            current_user.image_file = pic
        current_user.first_name = form_account.firstname.data
        current_user.last_name = form_account.surname.data
        current_user.username = form_account.username.data
        current_user.email = form_account.email.data
        db.session.commit()
        flash('your account has been updated successfully!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form_account.email.data = current_user.email
        form_account.username.data = current_user.username
        form_account.surname.data = current_user.last_name
        form_account.firstname.data = current_user.first_name
    image = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image, form=form_account)


@bp_main.route("/notifications")
@login_required
def notifications():
    return render_template('notifications.html', title='Notifications')

