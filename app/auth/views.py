from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timezone
import pytz
from uuid import uuid4
from . import auth
from .. import config, db
from ..models import User, Role
from .forms import LoginForm, RegisrationForm, ActivationForm
from app.auth.services import get_user_by_email, get_user_by_username


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.all_users'))
    
    if form.validate_on_submit():
        user: User = db.session.query(User).filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data) and user.active:
            user.last_sign_in = datetime.utcnow().replace(tzinfo=pytz.utc)
            
            db.session.add(user)
            db.session.commit()

            login_user(user, form.remember_me.data)
            
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            
            return redirect(next)
        
        flash('Invalid email or password.')
    else:
        if request.method != 'GET':
            flash('Please fill out the form properly!!!')
    
    return render_template('auth/login.html', form=form)


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisrationForm(request.form)

    if current_user.is_authenticated:
        return redirect(url_for('main.all_users'))

    if request.method == 'POST' and form.validate():
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

        flash('Successfully Registered. A mail has been sent please check your mailbox!!!')

        return redirect(url_for('auth.activate', username=user.username))

    else:
        if request.method != 'GET':
            flash("Internal System error")

    return render_template('auth/registration.html', form=form)


@auth.route('/activate/<string:username>', methods=['GET', 'POST'])
def activate(username):
    form = ActivationForm(request.form)

    if request.method == 'POST' and form.validate():
        user: User = db.session.query(User).filter_by(username=username).first()
        if user:
            if user.activation_code == form.activattion_code.data:
                user.active = True
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('auth.login'))
            else:
                flash("Wrong Activation Code. Try again!!!")
        else:
            flash("Internal System error")

    return render_template('auth/activate.html', form=form, username=username)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
