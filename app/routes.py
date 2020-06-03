from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
# This is to clear things up.
# The first app in "from app import app" refers to the app directory. The second one refers to the app variable in __init__.py
# __init__.py is like the representative of the whole directory. So when you want to get variables or classes in that module, you just refer it as app (the directory name) instead of its initial file name (__init__.py).
# If you want to refer other modules in app directory, use the directory name as a prefix (eg. app.forms, app.models, etc.).

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