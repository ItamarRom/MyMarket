import datetime
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
#The flask and framework coniguration settings are built inside a class
#for a more organized and manageable structure
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Setting the value of the path to the desired locatin of the DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Disabling a tracking feature which sends a signal when a change is about
    # to be made in the data base
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_PROTECTION = "strong"



