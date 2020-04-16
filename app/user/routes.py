import os
import secrets

from flask import current_app, url_for, render_template, request, flash, redirect, Blueprint
from flask_login import login_required, current_user

from app import db
from app.main.routes import role_required
from app.user.forms import UpdateAccountForm

from app.models import Book, Post, User, Review

# we create an instance of blueprint as main
bp_user = Blueprint('user', __name__)


def saving_pictures(profile_picture):
    hide_name = secrets.token_hex(6)
    _, f_extension = os.path.splitext(profile_picture.filename)
    p_pic = hide_name + f_extension
    pic_path = os.path.join(current_app.config['UPLOAD_FOLDER'], p_pic)
    profile_picture.save(pic_path)
    return p_pic


@bp_user.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    image = url_for('static', filename='profile_pictures/' + current_user.image_file)
    userid = current_user.get_id()
    bookings = []
    if current_user.roles == 'renter':
        bookings = Book.query.join(Post, Book.post_id == Post.post_id) \
            .join(User, User.user_id == Book.renter_user_id) \
            .add_columns( User.email, Post.title, Post.content,  Post.user_id, Book.book_id, Book.date_booked,
                         Book.status, Book.post_id, Book.price) \
            .filter_by(user_id=userid).all()
    elif current_user.roles == 'property_owner':
        bookings = Book.query.join(Post, Book.post_id == Post.post_id) \
            .join(User, User.user_id == Post.user_id) \
            .with_entities(Book.content, Book.email, Book.book_id, Book.status, Book.price, Book.renter_user_id)\
            .filter_by(user_id=userid).all()
    return render_template('profile.html', title='profile', image_file=image, bookings=bookings)


@bp_user.route('/my_posts')
@login_required
@role_required('property_owner')
def my_posts():
    userid = current_user.get_id()
    post_ids = Post.query.with_entities(Post.post_id).filter_by(user_id=userid).all()
    my_posts = []
    for post_id in post_ids:
        post_object = Post.query.get_or_404(post_id)
        my_posts.append(post_object)
    return render_template('my_posts.html', title='My Posts', posts=my_posts)


@bp_user.route('/bookings')
@login_required
@role_required('renter')
def my_bookings():
    userid = current_user.get_id()
    post_ids_of_bookings = Book.query.with_entities(Book.post_id).filter_by(renter_user_id=userid).all()
    posts_booked = []
    for post_id in post_ids_of_bookings:
        post_object = Post.query.get_or_404(post_id)
        posts_booked.append(post_object)
    return render_template('bookings.html', title='Book', bookings=posts_booked)


@bp_user.route("/update_account", methods=['GET', 'POST'])
@login_required
def update_account():
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
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form_account.email.data = current_user.email
        form_account.username.data = current_user.username
        form_account.surname.data = current_user.last_name
        form_account.firstname.data = current_user.first_name
    return render_template('update_account.html', title='account', form=form_account)
