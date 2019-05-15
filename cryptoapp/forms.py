from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cryptoapp.models import User

class registration_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Validators on registration so no errors will occur when trying to register dublicate data.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose another one')


class login_form(FlaskForm):
    email = StringField('Login with your Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Let's Go!")