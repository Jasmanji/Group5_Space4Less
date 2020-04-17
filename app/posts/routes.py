# Contributors: Kowther, Aure, Ariel
import os
import secrets

from flask import current_app, request, flash, redirect, url_for, render_template, Blueprint
from flask_login import login_required, current_user

from app import db
from app.main.routes import role_required
from app.posts.forms import PostForm, QuestionForm, AnswerForm, UpdatePostForm

from app.models import Post, User, Comment

# we create an instance of blueprint as main
bp_posts = Blueprint('posts', __name__)


# this is the function created to allow for pictures that a property owner uploads as part of the post to be saved.
# this function essentially creates a hex and attaches it onto the file extension (either jpg or png) and uses an OS
# join to save the route to the picture to the database as the image itself cannot be saved the image itself is saved
# in the POST_UPLOAD route (which is configured in the config.py) which  basically means the pictures themselves are
# saved to the static/post_pictures folder. Finally the path to the image is saved to the database and the post_image
# is returned
# Modified from: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/07-User
# -Account-Profile-Pic/flaskblog/routes.py.  Date retrieved: [2020/03/05]
def saving_pictures_post(post_picture):
    hide_name = secrets.token_hex(6)
    _, f_extension = os.path.splitext(post_picture.filename)
    post_image = hide_name + f_extension
    config = current_app.config
    post_path = os.path.join(config['POST_UPLOAD'], post_image)
    post_picture.save(post_path)
    return post_image


# beginning on the form_post.picture_for_posts.data line, the picture is requested from the user after which the
# saving_pictures_post() function created above is called to save the image to the folder and the path to the image
# is saved to the database
@bp_posts.route('/post', methods=['GET', 'POST'])
@login_required
@role_required('property_owner')
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


@bp_posts.route("/single_post/<post_id>", methods=['GET', 'POST'])
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


@bp_posts.route('/answer/<commentid>', methods=['GET', 'POST'])
@login_required
@role_required('property_owner')
def answer(commentid):
    answer_form = AnswerForm()
    comment = Comment.query.filter_by(comment_id=commentid).first()
    if answer_form.validate_on_submit():
        comment.answer = answer_form.answer.data
        db.session.commit()
        flash('you have successfully posted an answer', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('answer.html', form=answer_form)


@bp_posts.route("/update_post/<postid>", methods=['GET', 'POST'])
@role_required('property_owner')
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
        return redirect(url_for('user.my_posts'))
    elif request.method == 'GET':
        form_updatePost.title.data = post_obj.title
        form_updatePost.content.data = post_obj.content
        form_updatePost.location.data = post_obj.location
        form_updatePost.space_size.data = post_obj.space_size
    return render_template('update_post.html', title='Update a post', form=form_updatePost)
