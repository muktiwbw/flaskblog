from datetime import datetime
from app import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer

# The decorator (@) allows modification to a function without actually altering the original function. Much like references.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Now the UserMixin class is necessary because the Login extension needs some properties from a model to be authenticable. It's like Authenticable interface in Laravel (i think).
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # You can think of it like hasMany() in Laravel
    # But instead of writing down the backref with belongsToMany() to the child table, you use backref argument here
    # You want to avoid using terms and just stick to the model name backref naming to avoid confusion
    posts = db.relationship('Post', backref='user', lazy=True)

    def generate_reset_password_token(self, expiration_time=1800):
        secret_key = app.config['SECRET_KEY']
        payload = {'id': self.id}

        serializer = TimedJSONWebSignatureSerializer(secret_key, expiration_time)

        token = serializer.dumps(payload).decode('utf-8')

        return token

    # Adding static method decorator means you can call this method directly without making any class intance
    @staticmethod
    def verify_reset_password_token(token):
        secret_key = app.config['SECRET_KEY']
        serializer = TimedJSONWebSignatureSerializer(secret_key)

        try:
            payload = serializer.loads(token)
        except:
            return None

        return payload


    # This is what you'll see when you print the model
    # To make it easy to remember, just imagine that "repr" means representative,
    # although it might actually mean that lol
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

