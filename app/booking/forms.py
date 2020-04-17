# Contributors: Aure
# we want to import wtforms to help us with the validation
from flask_wtf import FlaskForm
# we need to import all the form fields as-well
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email


# this form is used by the renter to send a request for a property, their email is required along with some
# information in the content section, specifically, the length of time they need the property so the invoice properly
# reflects this. There are no restrictions on the length required in the content section
# wtform validation is included in the stringfield for the email
# the render_kw are there to add the placeholders for the string field type entries
# then once again the submit field is included.
class BookingRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "name@email.com"}
                        )
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    submit = SubmitField('send request')


# this form is where the property owner sends an invoice to the renter, the price must be an integer thus it is
# categorised as a IntegerField
# then once again the submit field is included
class SendInvoiceForm(FlaskForm):
    price = IntegerField('price',
                         validators=[DataRequired()],
                         render_kw={"placeholder": "price in pounds eg. 60"}
                         )
    submit = SubmitField('send request')
