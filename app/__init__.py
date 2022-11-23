from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment



# The app object is an instance of the Flask class imported at the top
app = Flask(__name__)

# Applying the configurations from the Config class inside the config.py file
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
# This variable is defined in order to tell flask_login the function name associated
# with the login view
login.login_view = 'login'
moment = Moment(app)
from app import routes, models




