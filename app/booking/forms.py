# we want to import wtforms to help us with the validation
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# we need to import all the form fields as-well
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class BookingRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "name@email.com"}
                        )
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    submit = SubmitField('send request')


class SendInvoiceForm(FlaskForm):
    price = IntegerField('price',
                         validators=[DataRequired()]
                         )
    submit = SubmitField('send request')