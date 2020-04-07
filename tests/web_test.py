import pytest
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from flask_testing import LiveServerTestCase
from app.models import User
import time

driver = webdriver.Chrome()

try:
    driver.get('http://http://127.0.0.1:5000')
    time.sleep(10)

    assert 'Home Page' == driver.title

finally:

    driver.quit()

