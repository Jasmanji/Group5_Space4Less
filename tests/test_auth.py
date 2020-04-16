# Contributors: Aure, Kowther
from flask import url_for
from app.models import User
from tests.test_main import BaseTestCase
from flask_login import current_user


class TestPosts(BaseTestCase):
    def test_login_fails_with_invalid_details(self):
        response = self.login(email='atlas@gmail.com', password='password')
        self.assertIn(b'Invalid username or password', response.data)

    def test_signup_page_valid(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_login_succeeds_with_valid_details(self):
        response = self.login(email='luna@gmail.com', password='5678')
        self.assertIn(b'Login successful!', response.data)

    def test_registration_valid_details(self):
        count = User.query.count()
        response = self.client.post(url_for('auth.signup'), data=dict(
            username=self.renter_data.get('Luna'),
            first_name=self.renter_data.get('rent'),
            last_name=self.renter_data.get('er'),
            email=self.renter_data.get('email'),
            password=self.renter_data.get('password'),
            roles=self.renter_data.get('role')
        ), follow_redirects=True)
        count2 = User.query.count()
        self.assertEqual(count2 - count, 0)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

    renter_data = dict(username='Luna', first_name="rent", last_name="er", email="luna@gmail.com",
                        roles='renter', password='5678')