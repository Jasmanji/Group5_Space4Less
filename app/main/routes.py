# next_page = request.args.get(
#                     'next')  # will get the page the user wanted to go to before they were redirected to login
#                 return redirect(next_page) if next_page else redirect(url_for(
#                     'main.home_page'))  # will redirect user to the page they requested before they tried to log in,
#                 # otherwise they will be redirected to home.
#
#



# the render template is to help us with returning an html template for a route
# the url_for is a function within flask that will find the exact location of routes for us
from flask import render_template, url_for, redirect, flash, Blueprint, request, current_app
import os
import secrets
from app import db
# we also need to import the forms
from app.main.forms import UpdateAccountForm, ReviewForm
from app.models import User, Post, Book, Review
from flask_login import current_user, login_required


# we create an instance of blueprint as main
bp_main = Blueprint('main', __name__)

# route for home page.
# this is where all the posts are displayed
# we select all posts to pass them in the home page.
@bp_main.route('/')
@bp_main.route('/home')
def home_page():
    posts = Post.query.all()
    return render_template('home.html', title='Home Page', posts=posts)



@bp_main.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        term = request.form.get("location")
        size = request.form.get("size")
        if term == "" and size == "":
            flash("Enter a location or size to search for")
            return redirect('/')
        elif term != "" and size == "":
            results = Post.query.filter(Post.location.contains(term)).all()
            size_displayed = "all sized spaces"
            location_displayed = term
        elif term == "" and size != "":
            results = Post.query.filter_by(space_size=size).all()
            size_displayed = size
            location_displayed = "all locations"
        elif term != "" and size != "":
            results = Post.query.filter_by(space_size=size, location=term).all()
            size_displayed = size
            location_displayed = term
        else:
            flash("No post found matching this data.")
            return redirect('/')
        return render_template('search.html', results=results, size_for_display=size_displayed,
                               location_for_display=location_displayed)
    else:
        return redirect(url_for('main.home_page'))




@bp_main.route('/aboutme')
def aboutme():
    return render_template('about_me.html')


@bp_main.route('/faq')
def faq():
    return render_template('FAQ.html')


def saving_pictures(profile_picture):
    hide_name = secrets.token_hex(6)
    _, f_extension = os.path.splitext(profile_picture.filename)
    p_pic = hide_name + f_extension
    pic_path = os.path.join(current_app.config['UPLOAD_FOLDER'], p_pic)
    profile_picture.save(pic_path)
    return p_pic


@bp_main.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    image = url_for('static', filename='profile_pictures/' + current_user.image_file)
    userid = current_user.get_id()
    bookings = []
    if current_user.roles == 'renter':
        bookings = Book.query.join(Post, Book.post_id == Post.post_id) \
            .join(User, User.user_id == Book.renter_user_id) \
            .add_columns(User.user_id, User.email, Post.title, Post.content, Book.book_id, Book.date_booked,
                         Book.status, Book.post_id) \
            .filter_by(user_id=userid).all()
    elif current_user.roles == 'property_owner':
        bookings = Book.query.join(Post, Book.post_id == Post.post_id) \
            .join(User, User.user_id == Post.user_id) \
            .with_entities(Book.content, Book.email, Book.book_id, Book.status, Book.price).filter_by(user_id=userid).all()
    return render_template('profile.html', title='profile', image_file=image, bookings=bookings)


@bp_main.route("/profile/<userid>", methods=['GET', 'POST'])
def view_profile(userid):
    user = User.query.get(userid)
    reviews = Review.query.filter_by(property_owner_user_id=userid) \
        .join(User, Review.renter_user_id == User.user_id) \
        .add_columns(Review.content, Review.stars, Review.date_posted, User.username, User.image_file,
                     Review.review_id) \
        .all()
    sum = 0
    number_of_reviews = 0
    star_number_tot = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'total': 0}
    if len(reviews) == 0:
        average = 'there are no reviews at this time'
    else:
        for review in reviews:
            for star_number in star_number_tot.keys():
                if star_number == review.stars:
                    star_number_tot[review.stars] += 1
                    star_number_tot['total'] += 1
            sum = sum + review.stars
            number_of_reviews = number_of_reviews + 1
        average = sum / number_of_reviews
    return render_template('view_profile.html', user=user, reviews=reviews, average=average,
                           star_number=star_number_tot)


@bp_main.route('/my_posts')
@login_required
def my_posts():
    userid = current_user.get_id()
    post_ids = Post.query.with_entities(Post.post_id).filter_by(user_id=userid).all()
    my_posts = []
    for post_id in post_ids:
        post_object = Post.query.get_or_404(post_id)
        my_posts.append(post_object)
    return render_template('my_posts.html', title='My Posts', posts=my_posts)


@bp_main.route("/update_account", methods=['GET', 'POST'])
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
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form_account.email.data = current_user.email
        form_account.username.data = current_user.username
        form_account.surname.data = current_user.last_name
        form_account.firstname.data = current_user.first_name
    return render_template('update_account.html', title='account', form=form_account)


@bp_main.route("/notifications/<user_id>")
@login_required
def notifications(user_id):
    return render_template('notifications.html', title='Notifications')


@bp_main.route('/rating/<property_owner_user_id>', methods=['GET', 'POST'])
def rate(property_owner_user_id):
    review_form = ReviewForm()
    user = User.query.get(current_user.get_id())

    if review_form.validate_on_submit():
        review = Review(content=review_form.content.data, stars=review_form.number.data, renter_user_id=user.user_id,
                        property_owner_user_id=property_owner_user_id)
        db.session.add(review)
        db.session.commit()
        flash('you have successfully posted a review!', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('rate.html', form=review_form)
