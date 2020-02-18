from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# creating the class for the sign up and log in forms
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)]
                           )
    firstname = StringField('First Name',
                            validators=[DataRequired()]
                            )
    surname = StringField('Surname',
                          validators=[DataRequired()]
                          )
    email = StringField('Email',
                        validators=[DataRequired(), Email()]
                        )
    password = PasswordField('Password',
                             validators=[DataRequired()]
                             )
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')]
                                     )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()]
                        )
    password = PasswordField('Password',
                             validators=[DataRequired()]
                             )
    remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')
