# Import modules
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

# Initialize flask app
app = Flask(__name__)

# Secret key for my app
app.config['SECRET_KEY'] = '862948fbdeb3cd375249b67465d67658'
# Database query string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize database model
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', {self.date_posted})"


# Routes
# Start with the route name, and then the handler below it
@app.route('/')
@app.route('/home')
def home():
    # Data simulation. Wouldn't be used in the future
    posts = [
        {
            'title': 'Blog Post One',
            'content': 'This is the first blog post.',
            'author': 'Abra',
            'date_posted': '12 May 2020'
        },
        {
            'title': 'Blog Post Two - Electric Boogaloo',
            'content': 'This is the second blog post.',
            'author': 'Cadabra',
            'date_posted': '13 May 2020'
        }
    ]

    # It's nice to encapsulate all the data into one dictionary
    data = {
        'posts': posts
    }

    return render_template('home.html', data=data)

@app.route('/about')
def about():
    title = 'About'

    data = {
        'title': title
    }

    return render_template('about.html', data=data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    data = {
        'form': form
    }

    return render_template('forms/registration.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'email@email.com' and form.password.data == 'password':
            flash(f'Welcome, {form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Authentication failed. Please enter your email and password correctly.', 'danger')

    data = {
        'form': form
    }

    return render_template('forms/login.html', data=data)

# This one's for running flask via python filename.py
if __name__ == '__main__':
    app.run(debug=True)