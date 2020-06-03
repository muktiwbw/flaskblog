from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize flask app
app = Flask(__name__)

# Secret key for my app
app.config['SECRET_KEY'] = '862948fbdeb3cd375249b67465d67658'
# Database query string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize database model
db = SQLAlchemy(app)

from app import routes