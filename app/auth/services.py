from .. import config, db
from ..models import User, Role
import pytz
from uuid import uuid4
from datetime import datetime


def get_user_by_email(email):
    user = db.session.query(User).filter_by(email=email).first()
    return user


def get_user_by_username(username):
    user = db.session.query(User).filter_by(username=username).first()
    return user


def create_a_user(form):
    user = User()
    user.email = form.email.data
    user.username = form.username.data
    user.password = form.password.data
    user.last_sign_in = datetime.utcnow().replace(tzinfo=pytz.utc)
    user.activation_code = str(uuid4())

    role = db.session.query(Role).get(2)
    user.role = role

    db.session.add(user)
    db.session.commit()

    return user