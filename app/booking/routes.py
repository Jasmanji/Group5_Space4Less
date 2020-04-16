import stripe # for payment
from flask import flash, redirect, url_for, render_template, request, Blueprint
from flask_login import login_required, current_user

from app import db
from app.booking.forms import BookingRequestForm, SendInvoiceForm

from app.models import Book

from app.main.routes import role_required

# for stripe booking
pub_key = 'pk_test_IzPesEUVXnPzY8a4Ecvr3J7C00bikUjRsi'
secret_key = 'sk_test_H8AjWDFHjwYjMkzloMCbE4qA00XSQyhQbS'
stripe.api_key = secret_key

# we create an instance of blueprint as main
bp_booking = Blueprint('booking', __name__)


@bp_booking.route('/book/<postid>', methods=['GET', 'POST'])
@login_required
@role_required('renter')
def book(postid):
    form_request_booking = BookingRequestForm()
    if form_request_booking.validate_on_submit():
        content = form_request_booking.content.data
        email = form_request_booking.email.data
        book = Book(renter_user_id=current_user.get_id(), post_id=postid, content=content, email=email)
        db.session.add(book)
        db.session.commit()
        flash(
            'You have successfully posted a request for the property! You can track your booking in your profile page!',
            'success')
        return redirect(url_for('user.profile'))
    return render_template('request_booking.html', form=form_request_booking)


@bp_booking.route('/send invoice/<bookid>', methods=['GET', 'POST'])
@login_required
@role_required('property_owner')
def send_invoice(bookid):
    form_send_invoice = SendInvoiceForm()
    book = Book.query.filter_by(book_id=bookid).first()

    if form_send_invoice.validate_on_submit():
        book.price = form_send_invoice.price.data
        book.status = 'payment required'
        db.session.commit()

        flash('You have successfully sent an invoice!', 'success')
        return redirect(url_for('main.home_page'))
    return render_template('send_invoice.html', form=form_send_invoice)


# This is the payment page. The renter, when he clicks on 'make payment' for a specific booking, it will
# bring them to this page, and they will make the payment specified in the invoice sent by the property owner
@bp_booking.route("/booking/<bookid>", methods=['GET', 'POST'])
@login_required
@role_required('renter')
def payment(bookid):
    invoice = Book.query.with_entities(Book.book_id, Book.price).filter_by(book_id=bookid).first()
    return render_template('payment.html', pub_key=pub_key, invoice=invoice)


@bp_booking.route('/pay/<bookid>', methods=['POST'])
@login_required
@role_required('renter')
def pay(bookid):
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    book = Book.query.filter_by(book_id=bookid).first()
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=book.price * 100,
        currency='gbp',
        description='Space4Less renting space'
    )
    book.status = 'payed'
    db.session.commit()
    flash('you have successfully payed for the property', 'success')
    return redirect(url_for('main.home_page'))
