import unittest
import os
import time
from app.config import TestConfig
import urllib.request
from abc import ABC
from os.path import join
from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from app import create_app, db
from app.models import User

user_one = dict(username='Luna', first_name="rent", last_name="er", email="luna@gmail.com",
                roles='renter', password='5678')
user_two = dict(username='Alan', first_name="proper", last_name="own", email="name@gmail.com",
                roles='property_owner', password='pass')
post_example = dict(title='property1', content='this is some content', location='earth', space_size='M')


class TestCase(LiveServerTestCase, ABC):
    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        self.driver = webdriver.Chrome(join(os.getcwd() + '/chromedriver'))
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        renter_one = dict(username='Jem', first_name="aname", last_name="alastname", email="Jem@gmail.com",
                          roles='renter', password='password')
        renter_two = dict(username='Lala', first_name="none", last_name="different", email="Lala@gmail.com",
                          roles='renter', password='1567')
        PO_one = dict(username='Hana', first_name="Hana", last_name="allow", email="Hana@gmail.com",
                      roles='property_owner', password='secure1')
        PO_two = dict(username='Amy', first_name="incomplete", last_name="profile", email="Amy@gmail.com",
                      roles='property_owner', password='apassword')

        post_one = dict(title='Atitle', content='this is a space', location='nw10', space_size='XS')

        db.session.add_all([self.renter_one, self.renter_two])
        db.session.add_all([self.PO_one, self.PO_two, post_one, post_example])
        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
