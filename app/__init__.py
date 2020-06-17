import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# In the future, don't use flask_uploads at all
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_mail import Mail

# Initialize flask app
app = Flask(__name__)

# Load environment
load_dotenv()

# Secret key for my app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Database query string
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = (os.getenv('MAIL_SENDER_NAME'), os.getenv('MAIL_SENDER_USERNAME'))

app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(app.root_path, 'static')


mail = Mail()
mail.init_app(app)

us_images = UploadSet('images', IMAGES)

configure_uploads(app, (us_images))

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