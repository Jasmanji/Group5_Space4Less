
# we want to import wtforms to help us with the validation
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# we need to import all the form fields as-well
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError






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




class QuestionForm(FlaskForm):
    question = TextAreaField('ask question here',
                             validators=[DataRequired()])
    submit = SubmitField('submit question'
                         '')


class AnswerForm(FlaskForm):
    answer = TextAreaField('Content',
                           validators=[DataRequired()])
    submit = SubmitField('submit answer')