import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt, us_images, mail
from app.forms import RegistrationForm, LoginForm, AccountUpdateForm, PostCreateForm, RPEmailForm, RPNewPasswordForm
from app.models import User, Post
# This is to clear things up.
# The first app in "from app import app" refers to the app directory. The second one refers to the app variable in __init__.py
# __init__.py is like the representative of the whole directory. So when you want to get variables or classes in that module, you just refer it as app (the directory name) instead of its initial file name (__init__.py).
# If you want to refer other modules in app directory, use the directory name as a prefix (eg. app.forms, app.models, etc.).

from flask_login import login_user, current_user, logout_user, login_required
from werkzeug import FileStorage
from flask_mail import Message

# Routes
# Start with the route name, and then the handler below it
@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=per_page, page=page)

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

        flash('Your profile has been updated', 'success')

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

@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostCreateForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            user=current_user
        )

        db.session.add(post)
        db.session.commit()

        flash(f'Your post, {form.title.data} has been created!', 'success')
        
        return redirect(url_for('home'))

    data = {
        'title': 'Create Post',
        'form': form,
        'legend': 'Create post'
    }
    
    return render_template('forms/post/create.html', data=data)

@app.route('/post/<int:id>')
def post_show(id):
    post = Post.query.get_or_404(id)

    data = {
        'title': f'{post.title} - {post.user.username}',
        'post': post
    }

    return render_template('post/show.html', data=data)

@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def post_update(id):
    post = Post.query.get_or_404(id)

    if post.user.id != current_user.id:
        abort(403)

    form = PostCreateForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()

        flash('Your post has been updated!', 'success')
        
        return redirect(url_for('post_show', id=id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    data = {
        'title': 'Update Post',
        'form': form,
        'legend': 'Update post'
    }

    return render_template('forms/post/create.html', data=data)

@app.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def post_delete(id):
    post = Post.query.get_or_404(id)

    if post.user.id != current_user.id:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted successfully!', 'success')

    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def post_user(username):
    page = request.args.get('page', 1, type=int)
    per_page = 5

    user = User.query.filter_by(username=username).first_or_404()

    # Similar to bash code, you can add backslash to use it as line break so that your code don't go too far right
    posts = Post.query.filter_by(user=user)\
                        .order_by(Post.date_posted.desc())\
                        .paginate(per_page=per_page, page=page)

    # It's nice to encapsulate all the data into one dictionary
    data = {
        'posts': posts,
        'user': user
    }

    return render_template('profile.html', data=data)

@app.route('/reset_password', methods=['GET', 'POST'])
def rp_email():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RPEmailForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        token = user.generate_reset_password_token()

        msg = Message('Reset Password')
        msg.add_recipient(email)
        msg.html = render_template('emails/reset_password.html', token=token)

        try:
            mail.send(msg)
        except:
            flash('There was an error when sending message!', 'danger')
            return redirect(url_for('rp_email'))

        flash('Verification token has been sent. Please check your inbox!', 'success')
        return redirect(url_for('rp_email'))

    data = {
        'title': 'Reset Password',
        'form': form
    }

    return render_template('forms/rp_email.html', data=data)

@app.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def rp_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RPNewPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=request.args.get('username')).first()

        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        db.session.commit()

        flash('You have successfully reset your password. Please login with your new password.', 'success')
        return redirect(url_for('login'))

    elif request.method == 'GET':
        # This method returns a payload contains user id in a form of dictionary
        payload = User.verify_reset_password_token(token)
        
        if not payload:
            flash('Unable to verify token. It is either invalid or has already expired.', 'danger')
            return redirect(url_for('rp_email'))

        user = User.query.get(payload['id'])

    data = {
        'title': 'Reset Password',
        'form': form,
        'user': user,
        'token': token
    }

    flash('Token is verified. Please enter your new password.', 'success')
    return render_template('forms/rp_password.html', data=data)