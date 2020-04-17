# Contributors: Aure, Kowther, Ariel
# we want to import wtforms to help us with the validation
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
# we need to import all the form fields as-well
from ukpostcodeutils import validation
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


# this allows for the postcodes to be validated to ensure they are indeed a valid UK postcode
# this is a piece of code which incorporated the use of the ukpostcodeutils dictionary
# and the function below was modified from: https://pypi.org/project/uk-postcode-utils/
def post_code_validator(form, field):
    if not validation.is_valid_postcode(field.data):
        raise ValidationError('Invalid UK Post Code')


# this is the form which allows the property owner to create a post
# all the aspects of the post form have the validation that they are a required field except for space size
#
# the location has the added validation using the fucntion above (post_code_validator) to ensure the location is a
# valid UK postcode.
# Space_size is a select field as the sizes for the posts are standardised and there are 6 options
# the pictures for posts takes the form of a filefield and it includes 2 bits of validation; that
# the picture is required and that they must have the extensions jpg or png only. finally there is a submit field to
# allow the user to post their property
class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    location = StringField('Postcode', validators=[DataRequired(), post_code_validator])

    space_size = SelectField('Space Size', validators=[DataRequired()], default=('0', 'Select'),
                             choices=[('0', 'Select'), ('Extra Small', 'XS'),
                                      ('Small', 'S'), ('Medium', 'M'),
                                      ('Medium Large', 'ML'), ('Large', 'L'),
                                      ('Extra Large', 'XL')])
    picture_for_posts = FileField('Post picture',
                                  validators=[FileRequired(), FileAllowed(['jpg', 'png'])]
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


class QuestionForm(FlaskForm):
    question = TextAreaField('ask question here',
                             validators=[DataRequired()])
    submit = SubmitField('submit question'
                         '')


class AnswerForm(FlaskForm):
    answer = TextAreaField('Content',
                           validators=[DataRequired()])
    submit = SubmitField('submit answer')
