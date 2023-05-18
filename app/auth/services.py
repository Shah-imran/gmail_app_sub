import pytz
from uuid import uuid4
from datetime import datetime
from sqlalchemy import and_
from flask import redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from .. import config, db
from ..models import User, Role
from app.settings import DEFAULT_USER_ROLE_ID, DEFAULT_API_ROLE_ID


def cross_auth_for_server(username, password):
    user = get_user_by_email(username) or get_user_by_username(password)

    if user is not None and user.verify_password(password):
        return True
    else:
        return False

def api_authentication(username, password):
    user: User = db.session.query(User).filter(
                and_(
                    User.username==username, 
                    User.role_id==DEFAULT_API_ROLE_ID
                )
            ).first()

    if user and user.verify_password(password):
        login_user(user, 0)
        return True
    else:
        return False
    

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