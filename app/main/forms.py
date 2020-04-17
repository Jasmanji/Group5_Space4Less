# Contributors: Aure

# we want to import wtforms to help us with the validation
from flask_wtf import FlaskForm
# we need to import all the form fields as-well
from wtforms import SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    content = TextAreaField('add review here',
                            validators=[DataRequired()])
    number = IntegerField('Rating',
                          validators=[DataRequired()]
                          )

    submit = SubmitField('submit review')
