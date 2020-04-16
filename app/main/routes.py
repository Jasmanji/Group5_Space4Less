# Contributors: Kowther, Ariel, Aure
# the render template is to help us with returning an html template for a route
# the url_for is a function within flask that will find the exact location of routes for us
import functools
from flask import render_template, url_for, redirect, flash, Blueprint, request
from app import db
from app.main.forms import ReviewForm # we also need to import the forms we will be using
from app.models import User, Post, Review, Book # the tables from the db we will use
from flask_login import current_user, login_required


# we create an instance of blueprint as main
bp_main = Blueprint('main', __name__)


# creating role required decorator to stop certain pages from being accessed depending on
# your role.
# with help from Victor!! Modified from: https://gist.github.com/VictorDarvariu/243773079e4e954bbda85ab505ebc270
def role_required(required_role):
    def role_decorator(func):                        # this is the decorator we are writing. The function we want to
                                                     # run is named 'func'
        @functools.wraps(func)                       # preserve information about the original function
        def function_wrapper(*args,
                             **kwargs):              # since the decorator needs to take argument 'role', we add the
                                                     # *args, kwargs
            if current_user.roles == required_role:  # if the user has the role required to access the page, we run
                                                     # the function.
                res = func(*args, **kwargs)
                return res                           # we need to return the arguments aswell as the function.
            else:                                    # if the user doesnt have the required role, we dont run the
                                                     # function.
                return render_template('errors/role.html', required_role=required_role)
        return function_wrapper
    return role_decorator


# route for home page.
# this is where all the posts are displayed
# we select all posts to pass them in the home page.
@bp_main.route('/')
@bp_main.route('/home')
def home_page():
    # ensures we always begin with page 1 and only integers are allowed as a page number
    page = request.args.get('page', 1, type=int)
    # per page defines how many posts are allowed in a single page and ensuring latest posts turn up first
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', title='Home Page', posts=posts)


# the pagination included here to restrict the number of results that appear per
# page and maintain the order such that the most recent posts turn up first
@bp_main.route('/search', methods=['POST', 'GET'])
def search():
    page = request.args.get('page', 1, type=int) # ensures the page begins at page 1 and pages are identified by
    # integers only
    if request.method == 'POST':
        term = request.form.get("location")
        size = request.form.get("size")
        if term == "" and size == "":
            flash("Enter a location or size to search for", 'danger')
            return redirect('/')
        elif term != "" and size == "":
            results = Post.query.filter(Post.location.contains(term))\
                .order_by(Post.date_posted.desc()).paginate(
                page=page, per_page=10)
            size_displayed = "all sized spaces"
            location_displayed = term
        elif term == "" and size != "":
            results = Post.query.filter_by(space_size=size)\
                .order_by(Post.date_posted.desc()).paginate(
                page=page, per_page=10)
            size_displayed = size
            location_displayed = "all locations"
        elif term != "" and size != "":
            results = Post.query.filter_by(space_size=size, location=term)\
                .order_by(Post.date_posted.desc()).paginate(
                page=page, per_page=10)
            size_displayed = size
            location_displayed = term
        return render_template('search.html', results=results, size_for_display=size_displayed,
                               location_for_display=location_displayed)
    else:
        return redirect(url_for('main.home_page'))

# the following two routes allow for the about me and FAQ pages to be rendered since
# they are only meant to be viewed as no interaction with the user is required
@bp_main.route('/aboutme')
def about_me():
    return render_template('about_me.html')


@bp_main.route('/faq')
def faq():
    return render_template('FAQ.html')


# This is the rating route. A user can add a review to a property owner from their profile
# if they have completed a payment for a booking with that property owner.
# for every booking you are only allowed one rating. The review form contains a place you can
# write the review, and a star rating you select.
# We get the property_owner id from looking at who posted the post that is being reviewed.
# The renter's id will simply be the current user's id
# With this, and the form submitted, we can create a review which we can commit to the db.
# We also change the status of the booking to 'booking complete', as this means the renter can no
# longer submit a review for that specific booking.
@bp_main.route('/rating/<bookid>', methods=['GET', 'POST'])
@login_required
@role_required('renter')
def rate(bookid):
    review_form = ReviewForm()
    property_owner_user_id = Book.query.filter_by(book_id=bookid).join(Post, Post.post_id==Book.post_id)\
        .with_entities(Post.user_id)
    user = User.query.get(current_user.get_id())
    book= Book.query.filter_by(book_id=bookid).first()
    if review_form.validate_on_submit():
        review = Review(content=review_form.content.data, stars=review_form.number.data, renter_user_id=user.user_id,
                        property_owner_user_id=property_owner_user_id)
        book.status = 'booking complete'
        db.session.add(review)
        db.session.commit()
        flash('you have successfully posted a review!', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('rate.html', form=review_form)


# This is the view_profile function, which is to see the profiles of property owners that have posted
# a certain post. It is mostly to look at reviews to see if they are trustworthy- had any
# positive feedback...
# for each property owner, we will have a summary display of all the ratings' statistics, aswell as
# all the reviews.
# The star_number_tot is a dictionary that contains the number of renters that have voted:
# 1 star, 2,3,4 or 5 starts, plus the total number of stars.
# We loop through all reviews to count how many in each category. We then can calculate the
# average by each time adding the number of stars to a total sum, which is then divided by
# the total number of ratings ('total' in star_number_tot dict). The average is also rounded to 1dp
@bp_main.route("/view_profile/<userid>", methods=['GET', 'POST'])
@login_required
def view_profile(userid):
    user = User.query.get(userid)
    reviews = Review.query.filter_by(property_owner_user_id=userid) \
        .join(User, Review.renter_user_id == User.user_id) \
        .add_columns(Review.content, Review.stars, Review.date_posted, User.username, User.image_file,
                     Review.review_id) \
        .all()
    summation = 0
    star_number_tot = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'total': 0}
    if len(reviews) == 0: # if there are no reviews, there's no average. This is to prevent division by 0
        average = 'there are no reviews at this time'
    else:
        for review in reviews: # in each review, we look at the number of stars it had.
            for star_number in star_number_tot.keys():
                if star_number == review.stars: # we find that star number in the dictionary which it corresponds to
                    star_number_tot[review.stars] += 1 # and add one to that star number it corresponds to
                    star_number_tot['total'] += 1 # and one to the total number of reviews
            summation = summation + review.stars  # we add the total number of stars to our total sum of stars
        average = round(summation / star_number_tot['total'],1)  # and do the average by dividing
        # the sum by the total number of stars, and rounding it to 1dp.
    return render_template('view_profile.html', user=user, reviews=reviews, average=average,
                           star_number=star_number_tot)
