from .. import config, db
from ..models import User


def get_user_by_email(email):
    user = db.session.query(User).filter_by(email=email).first()
    return user


def get_user_by_username(username):
    user = db.session.query(User).filter_by(username=username).first()
    return user
