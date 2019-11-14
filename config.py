import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Class for configuration items
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # take location of application database - if URL not found then configue database named app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # disable feature - signal application each time a change is about to be made to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # add email server details

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT')or 25)
    # enable encryption
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['seancolgo@gmail.com']

    # Pagination config variables
    POSTS_PER_PAGE = 20

    # define supported languages
    LANGUAGES = ['en', 'es']

    # azure translation service key
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    # configure elasticsearch
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    

