"""Flask config class."""
from os.path import dirname, abspath, join

class Config(object):

    # we also need to set up a secret key for our application.
    # This will protect against modifying cookies and cross-site request forgery attacks...
    """Set Flask base configuration"""
    SECRET_KEY = '9hQaY2nGqS9YQbs_b033vA'

    # to generate a secret key: (in python console)
    # import secrets
    # secrets.token_urlsafe(16)
    # General Config DEBUG = False TESTING = False
    # Forms config
    # we also need a secret key for the forms
    WTF_CSRF_SECRET_KEY = 'lCgqy2NPRYY5NYkk25bhuQ'

    # Database config
    CWD = dirname(abspath(__file__))
    # choosing path of where database will be and its name
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(CWD, 'spaceless.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    TESTING = True


class DevConfig(Config):
    DEBUG = True