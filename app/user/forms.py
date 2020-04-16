# Contributors:
# we want to import wtforms to help us with the validation
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# we need to import all the form fields as-well
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


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
