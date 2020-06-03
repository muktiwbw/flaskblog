from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

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
                                DataRequired(),
                                Length(min=8)
                            ])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')