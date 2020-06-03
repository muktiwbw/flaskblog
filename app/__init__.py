from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize flask app
app = Flask(__name__)

# Secret key for my app
app.config['SECRET_KEY'] = '862948fbdeb3cd375249b67465d67658'
# Database query string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize database model
db = SQLAlchemy(app)

# Initialize bcrypt module
bcrypt = Bcrypt(app)

# Initialize login modul
login_manager = LoginManager(app)
# These two below are responsible for redirecting user if they're not authenticated
# login_view tells the app to redirect to specified route method
# login_message_category tells the app to show message in specified color or theme
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes