# Contributors: Kowther
import unittest

from flask import url_for
from flask_testing import TestCase
from app import create_app, db

from app.models import User
from app.config import TestConfig

from flask_login import current_user, login_user, logout_user


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        # Called before every test
        db.create_all()
        # test data
        self.propertyowner = User(username="Atlas", first_name="property", last_name="owner", email="atlas@gmail.com",
                                  roles="property_owner")
        self.propertyowner.set_password('1234')

        self.renter = User(username="Luna", first_name="rent", last_name="er", email="luna@gmail.com",
                           roles="renter")
        self.renter.set_password('5678')
        db.session.add(self.propertyowner)
        db.session.add(self.renter)
        db.session.commit()

    def tearDown(self):
        # to remove test data from database
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.client.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.client.get(
            '/logout',
            follow_redirects=True
        )

    def signup(self, username, last_name, first_name, email, password, roles):
        return self.client.post(
            '/signup',
            data=dict(username=username, first_name=first_name, last_name=last_name, email=email, password=password,
                      roles=roles),
            follow_redirects=True
        )

    def test_faq_page_valid(self):
        response = self.client.get('/faq')
        self.assertEqual(response.status_code, 200)

    def test_about_me_page_valid(self):
        response = self.client.get('/aboutme')
        self.assertEqual(response.status_code, 200)

    # propertyOwner_data = dict(username='Alan', first_name="proper", last_name="own", email="name@gmail.com",
    #                           roles='property_owner', password='pass')
    # post_data = dict(title='property1', content='this is some content', location='earth', space_size='M')


if __name__ == '__main__':
    unittest.main()