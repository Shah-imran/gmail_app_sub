from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Date, Integer, Boolean, DateTime, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.schema import FetchedValue
from sqlalchemy.sql import func
from flask_login import UserMixin
import datetime
import uuid

from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic', passive_deletes=False)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False, unique=True, index=True)
    username = Column(String(64), nullable=False, unique=True, index=True)
    active = Column(Boolean, nullable=False, default=False)
    password_hash = Column(String(128))
    last_sign_in = Column(DateTime(timezone=True), nullable=True)
    time_created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    activation_code = Column(String(128), nullable=True, default=None)

    role_id = Column(Integer, db.ForeignKey('roles.id'))
    servers = db.relationship('Server', backref='user', lazy='dynamic', passive_deletes=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User {self.username} {self.email}"


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    active = Column(Boolean, default=False)
    device_count = Column(Integer, default=0)
    description = Column(Text, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    servers = db.relationship('Server', backref='sub_type', lazy='dynamic', passive_deletes=False)

    def date_to_string(self, date):
        return date.strftime("%m-%d-%Y")

    def __repr__(self):
        return f"Subscription {self.name} {self.device_count} {self.description}"
    

class Server(db.Model):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    ip_address = Column(String(16), nullable=False)
    active = Column(Boolean, default=False, nullable=False)
    assigned = Column(Boolean, default=False, nullable=False)
    description = Column(Text, nullable=True)
    sub_end_date = Column(Date, default=None)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=True)
    subs_id = Column(Integer, db.ForeignKey('subscriptions.id'), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
