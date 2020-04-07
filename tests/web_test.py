import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_registration(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000")
        self.assertTrue("Home Page", driver.title)
        self.driver.find_element_by_link_text("Signup").click()
        time.sleep(2)
        # Test person
        username = "Jem"
        first_name = "aname"
        last_name = "alastname"
        email = "Jem@gmail.com"
        password = "password"
        confirm = "password"
        role = "Property Owner"

        # Fill in registration form
        self.driver.find_element_by_name("username").send_keys(username)
        self.driver.find_element_by_id("firstname").send_keys(first_name)
        self.driver.find_element_by_id("surname").send_keys(last_name)
        self.driver.find_element_by_id("email").send_keys(email)
        role_select = Select(self.driver.find_element_by_id("role"))
        role_select.select_by_visible_text(role)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("confirm_password").send_keys(confirm)
        self.driver.find_element_by_id("submit").click()
        self.driver.implicitly_wait(10)


if __name__ == '__main__':
    unittest.main()
