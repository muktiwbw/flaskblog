import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, us_images
from app.forms import RegistrationForm, LoginForm, AccountUpdateForm
from app.models import User, Post
# This is to clear things up.
# The first app in "from app import app" refers to the app directory. The second one refers to the app variable in __init__.py
# __init__.py is like the representative of the whole directory. So when you want to get variables or classes in that module, you just refer it as app (the directory name) instead of its initial file name (__init__.py).
# If you want to refer other modules in app directory, use the directory name as a prefix (eg. app.forms, app.models, etc.).

from flask_login import login_user, current_user, logout_user, login_required
from werkzeug import FileStorage

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # This returns the data submitted from view
    # If nothing is submitted or this method is accessed through GET method, it returns False
    form = RegistrationForm()

    # This basically says if the form data pass various validations
    # validate_on_submit() will return True when:
    #   1. Form is submitted
    #   2. Form values passed the validations
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Assign fields' value
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password
        )
        # Add data instance to queue
        db.session.add(user)
        # Commit (or save) to db
        db.session.commit()

        # f'string {var}' gives you ability to encapsulate variables into a string
        # Only works in Python 3.6 and above
        flash(f'Account created for {user.username}!', 'success')
        return redirect(url_for('login'))

    data = {
        'form': form
    }

    return render_template('forms/registration.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        # Model.query.filter_by(fieldname=value) => to query using specific field
        # Model.query.get(id) => to query using id
        # For filter_by(), don't forget to chain it with all() or first(). Don't need them for get()
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            flash(f'Welcome, {user.username}!', 'success')

            # Get query string called "next"
            next_route = request.args.get('next')

            # It's called ternary conditional operator where you use if-else in one line
            return redirect(next_route) if next_route else redirect(url_for('home'))
        else:
            flash('Authentication failed. Please enter your email and password correctly.', 'danger')

    data = {
        'form': form
    }

    return render_template('forms/login.html', data=data)

@app.route('/logout')
def logout():
    logout_user()
    
    flash('You are logged out.', 'success')

    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()

    # validate_on_submit() already represents POST method, so no need to specify
    if form.validate_on_submit():
        # Remove current image if user has changed it once
        current_image_file = os.path.join(app.root_path, 'static/images/profile', current_user.image_file)
        
        if current_user.image_file != 'default.jpg' and os.path.isfile(current_image_file):
            os.remove(current_image_file)

        # Save image, returns image filename
        filename = us_images.save(form.image.data, folder='profile', name=f'ava-{secrets.token_hex(8)}.').split('/')[1]

        # Flask_login allows to update model's value through session. This will also update the session immediately
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.image_file = filename

        db.session.commit()

        return redirect(url_for('account'))

    elif request.method == 'GET':
        # This is the way to populate field's value instead of doing it on the html file
        form.username.data = current_user.username
        form.email.data = current_user.email

    data = {
        'title': 'Account Page',
        'form': form
    }

    return render_template('account.html', data=data)