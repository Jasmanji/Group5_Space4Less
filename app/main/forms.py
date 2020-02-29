# we want to import wtforms to help us with the validation
from flask_wtf import FlaskForm
# we need to import all the form fields as-well
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# creating the class for the sign up form, which will inherit from the class FlaskForm to be representative of our form
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

    role = SelectField('Role', default=('0', 'Select'), choices=[('0', 'Select'), ('1', 'Property Owner'),
                                                                 ('2', 'Renter')]

                       )

    # we also need a submit button to send the information
    submit = SubmitField('Sign Up')


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

# when we use this forms we need to use a secret key
