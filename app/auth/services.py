import pytz
from uuid import uuid4
from datetime import datetime
from flask import redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from .. import config, db
from ..models import User, Role
from app.settings import DEFAULT_USER_ROLE_ID


def redirect_user():
    path = 'main.dashboard' if current_user.role.name == 'User' else 'main.all_users'
    return redirect(url_for(path))


def get_user_by_email(email):
    user = db.session.query(User).filter_by(email=email).first()
    return user


def get_user_by_username(username):
    user = db.session.query(User).filter_by(username=username).first()
    return user


def reset_password(form):
    user: User = db.session.query(User).get(current_user.get_id())
    user.password = form.password.data

    db.session.add(user)
    db.session.commit()

def create_a_user(form):
    user = User()
    user.email = form.email.data
    user.username = form.username.data
    user.password = form.password.data
    user.last_sign_in = datetime.utcnow().replace(tzinfo=pytz.utc)
    user.activation_code = str(uuid4())

    role = db.session.query(Role).get(DEFAULT_USER_ROLE_ID)
    user.role = role

    db.session.add(user)
    db.session.commit()

    return user