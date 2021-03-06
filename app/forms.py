from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[
                                DataRequired(),
                                Length(min=2, max=20)
                            ])
    
    email = StringField('Email',
                            validators=[
                                DataRequired(),
                                Email()
                            ])
    
    password = PasswordField('Password',
                            validators=[
                                DataRequired(),
                                Length(min=8)
                            ])

    confirm_password = PasswordField('Confirm Password',
                            validators=[
                                DataRequired(),
                                EqualTo('password')
                            ])

    submit = SubmitField('Sign Up')

    # Custom validations
    # def validate_fieldname(self, fieldname):
    #     if True:
    #         raise ValidationError('messages')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username has already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email has already taken.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators=[
                                DataRequired(),
                                Email()
                            ])
    
    password = PasswordField('Password',
                            validators=[
                                DataRequired()
                            ])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class AccountUpdateForm(FlaskForm):
    username = StringField('Username',
                            validators=[
                                DataRequired(),
                                Length(min=2, max=20)
                            ])

    email = StringField('Email',
                            validators=[
                                DataRequired(),
                                Email()
                            ])

    image = FileField('Profile picture', 
                            validators=[
                                FileAllowed([
                                    'jpg', 'jpeg', 'png'
                                ])
                            ])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError('Username has already taken.')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('Email has already takne.')

class PostCreateForm(FlaskForm):
    title = StringField('Title', 
                            validators=[
                                DataRequired()
                            ])
    
    content = TextAreaField('Content',
                            validators=[
                                DataRequired()
                            ])

    submit = SubmitField('Submit')

class RPEmailForm(FlaskForm):
    email = StringField('Email', validators=[
                                    DataRequired()
                                ])

    submit = SubmitField('Send Verification Token')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if not user:
            raise ValidationError('Email is not registered!')

class RPNewPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
                                            DataRequired(),
                                            Length(min=8)
                                        ])

    confirm_password = PasswordField('Confirm password', validators=[
                                                            DataRequired(),
                                                            EqualTo('password')
                                                        ])

    submit = SubmitField('Reset Password')