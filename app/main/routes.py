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
from app.main.forms import UpdateAccountForm, PostForm, UpdatePostForm, QuestionForm, AnswerForm, ReviewForm
from app.models import User, Post, Book, Comment, Review
from flask_login import current_user, login_required

# import stripe
#
# #for stripe booking
# pub_key = 'pk_test_IzPesEUVXnPzY8a4Ecvr3J7C00bikUjRsi'
# secret_key = 'sk_test_H8AjWDFHjwYjMkzloMCbE4qA00XSQyhQbS'
# stripe.api_key = secret_key


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


def saving_pictures_post(post_picture):
    hide_name = secrets.token_hex(6)
    _, f_extension = os.path.splitext(post_picture.filename)
    post_image = hide_name + f_extension
    config = current_app.config
    post_path = os.path.join(config['POST_UPLOAD'], post_image)
    post_picture.save(post_path)
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
        flash('you have successfully posted your space!!', 'success')
        return redirect(url_for('main.home_page'))
    image = url_for('static', filename='post_pictures/' + str(form_post.picture_for_posts))
    return render_template('post.html', title='Post', content='content', image=image, form=form_post)


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


@bp_main.route("/update_post/<postid>", methods=['GET', 'POST'])
def update_post(postid):
    post_obj = Post.query.get(postid)
    form_updatePost = UpdatePostForm()
    if form_updatePost.validate_on_submit():
        if form_updatePost.picture_for_posts.data:
            file = request.files['picture_for_posts']
            pic = saving_pictures_post(file)
            post_obj.image = pic
        post_obj.title = form_updatePost.title.data
        post_obj.content = form_updatePost.content.data
        post_obj.location = form_updatePost.location.data
        post_obj.space_size = form_updatePost.space_size.data
        db.session.commit()
        flash('You have successfully updated your post!', 'success')
        return redirect(url_for('main.my_posts'))
    elif request.method == 'GET':
        form_updatePost.title.data = post_obj.title
        form_updatePost.content.data = post_obj.content
        form_updatePost.location.data = post_obj.location
        form_updatePost.space_size.data = post_obj.space_size
    return render_template('update_post.html', title='Update a post', form=form_updatePost)


@bp_main.route("/notifications/<user_id>")
@login_required
def notifications(user_id):
    return render_template('notifications.html', title='Notifications')


@bp_main.route("/single_post/<post_id>", methods=['GET', 'POST'])
@login_required
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get(current_user.get_id())
    form_question = QuestionForm()
    comments = Comment.query.filter_by(post_id=post_id) \
        .join(User, Comment.renter_user_id == User.user_id) \
        .add_columns(Comment.question, Comment.answer, Comment.date_posted, User.username, User.image_file,
                     Comment.comment_id) \
        .all()
    if form_question.validate_on_submit():
        comment = Comment(question=form_question.question.data, renter_user_id=user.user_id, post_id=post.post_id)

        db.session.add(comment)
        db.session.commit()
        flash('you have successfully commented on the post', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('single_post.html', title=post.title, post=post, form=form_question, comments=comments)


@bp_main.route('/answer/<commentid>', methods=['GET', 'POST'])
def answer(commentid):
    answer_form = AnswerForm()
    comment = Comment.query.filter_by(comment_id=commentid).first()
    if answer_form.validate_on_submit():
        comment.answer = answer_form.answer.data
        db.session.commit()
        flash('you have successfully posted an answer', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('answer.html', form=answer_form)


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
