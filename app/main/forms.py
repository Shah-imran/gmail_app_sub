from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.auth.services import (
    get_user_by_email, 
    get_user_by_username
)

from app.main.services import get_one_server


class UserCreationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    re_password = PasswordField('Re-password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create')

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


class ServerCreationForm(FlaskForm):
    ip_address = StringField('IP Address', validators=[DataRequired(), Length(1, 16)])
    description = StringField('Desciption')
    submit = SubmitField('Sign Up')

    def validate_ip_address(self, ip_address):
        server = get_one_server(ip_address.data)

        if server:
            flash('This IP Address already exists.')
            raise ValidationError('This IP Address already exists.')