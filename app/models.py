from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    machine_uuid = db.Column(db.String(128))
    processor_id = db.Column(db.String(128))
    end_date = db.Column(db.Date())
    active = db.Column(db.Boolean(), default=False)
    last_sign_in = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def date_to_string(self, date):
        return date.strftime("%m-%d-%Y")

    def __repr__(self):
        return '<User %r>' % self.email

class Version(db.Model):
    __tablename__= 'version'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    link = db.Column(db.Text)
    size = db.Column(db.Integer)
    download = db.Column(db.Integer, nullable=False, default=0)

class WUM_Version(db.Model):
    __tablename__= 'wum_version'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    link = db.Column(db.Text)
    size = db.Column(db.Integer)
    download = db.Column(db.Integer, nullable=False, default=0)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
