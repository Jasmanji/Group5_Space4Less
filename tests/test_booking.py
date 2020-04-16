from flask import url_for
from flask_login import current_user

from tests.test_main import BaseTestCase


class TestBooking(BaseTestCase):

    def test_booking_is_a_success(self):
        self.login(email=self.renter.email, password=self.renter.password)
        response = self.client.post(
            '/book/1',
            data=dict(renter_user_id=current_user.get_id(), post_id=1, email='renter@gmail.com', content='content'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

