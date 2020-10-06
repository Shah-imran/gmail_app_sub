from flask import render_template, redirect, request, url_for, flash
from . import main
from ..models import Subscriber
from flask_login import login_user, logout_user, login_required, current_user


@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.pending_request'))
    return render_template('auth/login.html')

@main.route('/pending_request', methods=['GET'], defaults={"page": 1})
@main.route('/pending_request/<int:page>', methods=['GET'])
@login_required
def pending_request(page):
    per_page = 1
    subscribers = Subscriber.query.filter_by(
        active=False).paginate(page,per_page,error_out=False)
    return render_template('pending_request.html', subscribers=subscribers, page=page)


@main.route('/active_user', methods=['GET'])
@login_required
def active_user():
    return render_template('active_user.html')
