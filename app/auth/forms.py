from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.auth.services import get_user_by_email, get_user_by_username


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    re_password = PasswordField('Re-password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = get_user_by_username(username.data)
        if user:
            flash('That username is taken. Please choose another.')
            raise ValidationError('That username is taken. Please choose another.')

    def validate_email(self, email):
        user = get_user_by_email(email.data)
        if user:
            flash('That email is taken. Please choose another.')
            raise ValidationError('That email is taken. Please choose another.')
        

class ActivationForm(FlaskForm):
    activattion_code = StringField("Activation Code", validators=[DataRequired()])
    submit = SubmitField('Activate')