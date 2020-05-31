# Import Flask module
from flask import Flask

# Initialize flask app
app = Flask(__name__)

# Routes
# Start with the route name, and then the handler below it
@app.route('/')
def home():
    return 'Home Page'

@app.route('/about')
def about():
    return 'About Page'

# This one's for running flask via python filename.py
if __name__ == '__main__':
    app.run(debug=True)