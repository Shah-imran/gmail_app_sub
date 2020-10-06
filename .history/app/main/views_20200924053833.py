from flask import render_template
from . import main
from flask_login import login_user, logout_user, login_required, current_user


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('pending_request.html')
    return render_template('index.html')

@main.route('/pending_request', methods=['GET'])
def pending_request():
    return render_template('pending_request.html')

@main.route('/active_user', methods=['GET'])
def active_user():
    return render_template('active_user.html')
