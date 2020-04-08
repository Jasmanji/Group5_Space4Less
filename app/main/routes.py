# next_page = request.args.get(
#                     'next')  # will get the page the user wanted to go to before they were redirected to login
#                 return redirect(next_page) if next_page else redirect(url_for(
#                     'main.home_page'))  # will redirect user to the page they requested before they tried to log in,
#                 # otherwise they will be redirected to home.
#
#



# the render template is to help us with returning an html template for a route
# the url_for is a function within flask that will find the exact location of routes for us
from flask import render_template, url_for, redirect, flash, Blueprint, request
from app import db
# we also need to import the forms
from app.main.forms import ReviewForm
from app.models import User, Post, Review
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
