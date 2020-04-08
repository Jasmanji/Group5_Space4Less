# we want to import wtforms to help us with the validation
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# we need to import all the form fields as-well
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


# creating the class for the sign up form, which will inherit from the class FlaskForm to be representative of our form
# from app.models import User


class RegistrationForm(FlaskForm):
    # we will create form fields to validate specific things
    # the username is going to be a string field.
    # the first input is 'Username' which is the name of the filed. This will be used as the label in our HTML.
    # We then want to put some limits, we do this using validators: which will be a list of validations we want
    # to check.
    # the DataRequired validator will be used to check the user put an input.
    # the length gives a min and max amount the username can be.
    # the render_kw are there to add the placeholders for the string field type entries but the same is not applicatble
    # for the selectfield thus a different method (default) was used.
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Enter a unique username"}
                           )
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)],
                            render_kw={"placeholder": "Name"}
                            )
    surname = StringField('Surname',
                          validators=[DataRequired()],
                          render_kw={"placeholder": "Surname"}
                          )
    # the validator Email() will check if the input email is a valid email
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "name@email.com"}
                        )
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Must be at least 4 characters"}
                             )
    # the EqualTo('password') will make sure that it contains the same content as the password field
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "Re-Enter Password"}
                                     )

    role = SelectField('Role', default=('0', 'Select'), choices=[('0', 'Select'), ('property_owner', 'Property Owner'),
                                                                 ('renter', 'Renter')]
                       )

    # we also need a submit button to send the information
    submit = SubmitField('Sign Up')

    # checking username is unique


#    def validate_username(self, username):
#       user = User.query.filter_by(username=username.data).first()
#      if user:
#         raise ValidationError('This username is already taken! please choose another username')

# ensuring email is unique
#  def validate_email(self, email):
#     user = User.query.filter_by(username=email.data).first()
#    if user:
#       raise ValidationError('An account has already been created with this email.')


# creating the LoginForm class
class LoginForm(FlaskForm):
    # we will use the email as an input to log in, and a password
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Enter Your Email Here"}
                        )
    password = PasswordField('Password',
                             validators=[DataRequired()], render_kw={"placeholder": "Enter Your Password Here"}
                             )
    # this will allow the users to stay logged in after their browser closes using a secure login
    # this will be a boolean field
    remember = BooleanField('Remember Me')
    # again, we will need a submit button
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Enter a unique username"}
                           )
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)],
                            render_kw={"placeholder": "Name"}
                            )
    surname = StringField('Surname',
                          validators=[DataRequired()],
                          render_kw={"placeholder": "Surname"}
                          )
    # the validator Email() will check if the input email is a valid email
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "name@email.com"}
                        )

    # for adding a picture
    picture = FileField('Profile picture',
                        validators=[FileAllowed(['jpg', 'png'])]

                        )

    # we also need a submit button to send the information
    submit = SubmitField('Update')


class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    location = TextAreaField('location', validators=[DataRequired()])
    space_size = SelectField('Space Size', validators=[DataRequired()], default=('0', 'Select'),
                             choices=[('0', 'Select'), ('Extra Small', 'XS'),
                                      ('Small', 'S'), ('Medium', 'M'),
                                      ('Medium Large', 'ML'), ('Large', 'L'),
                                      ('Extra Large', 'XL')])
    picture_for_posts = FileField('Post picture',
                                  validators=[FileAllowed(['jpg', 'png'])]
                                  )
    submit = SubmitField('Post')


class UpdatePostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    location = TextAreaField('location', validators=[DataRequired()])
    space_size = SelectField('Space Size', default=('0', 'Select'), choices=[('0', 'Select'), ('Extra Small', 'XS'),
                                                                             ('Small', 'S'), ('Medium', 'M'),
                                                                             ('Medium Large', 'ML'), ('Large', 'L'),
                                                                             ('Extra Large', 'XL')])
    picture_for_posts = FileField('Post picture',
                                  validators=[FileAllowed(['jpg', 'png'])]
                                  )
    submit = SubmitField('Update')


# class BookingRequestForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()],
#                         render_kw={"placeholder": "name@email.com"}
#                         )
#     content = TextAreaField('Content',
#                             validators=[DataRequired()])
#     submit = SubmitField('send request')
#
#
# class SendInvoiceForm(FlaskForm):
#     price = IntegerField('price',
#                          validators=[DataRequired()]
#                          )
#     submit = SubmitField('send request')


class EmailForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "name@email.com"}
                        )
    submit = SubmitField('Send Email')


class PasswordReset(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Must be at least 4 characters"}
                             )
    # the EqualTo('password') will make sure that it contains the same content as the password field
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "Re-Enter Password"}
                                     )
    submit = SubmitField('Update Password'
                         '')


class QuestionForm(FlaskForm):
    question = TextAreaField('ask question here',
                             validators=[DataRequired()])
    submit = SubmitField('submit question'
                         '')


class AnswerForm(FlaskForm):
    answer = TextAreaField('Content',
                           validators=[DataRequired()])
    submit = SubmitField('submit answer')


class ReviewForm(FlaskForm):
    content = TextAreaField('add review here',
                            validators=[DataRequired()])
    number = IntegerField('Rating',
                          validators=[DataRequired()]
                          )

    submit = SubmitField('submit review')
