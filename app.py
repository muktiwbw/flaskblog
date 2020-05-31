# Import Flask module
from flask import Flask, render_template

# Initialize flask app
app = Flask(__name__)

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

# This one's for running flask via python filename.py
if __name__ == '__main__':
    app.run(debug=True)