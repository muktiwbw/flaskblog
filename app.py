# Import modules
from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

# Initialize flask app
app = Flask(__name__)

# Secret key for my app
app.config['SECRET_KEY'] = '862948fbdeb3cd375249b67465d67658'

# Routes
# Start with the route name, and then the handler below it
@app.route('/')
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

    data = {
        'form': form
    }

    return render_template('forms/registration.html', data=data)

@app.route('/login')
def login():
    form = LoginForm()

    data = {
        'form': form
    }

    return render_template('forms/login.html', data=data)

# This one's for running flask via python filename.py
if __name__ == '__main__':
    app.run(debug=True)