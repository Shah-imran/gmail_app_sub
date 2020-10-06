from flask import render_template
from . import main
from ..models import Subscriber
from flask_login import login_user, logout_user, login_required, current_user


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('pending_request.html')
    return render_template('index.html')

@main.route('/pending_request', methods=['GET'], defaults={"page": 1})
@main.route('/pending_request/<int:page>', methods=['GET'])
@login_required
def pending_request(page):
    per_page = 1
    subscribers = Subscriber.query.filter_by(active=False).paginate(page,per_page,error_out=False)
    return render_template('pending_request.html')

@app.route('/', methods=['GET'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET'])
def index(page):
    per_page = 10
    posts = Posts.query.order_by(Posts.time.desc()).paginate(page,per_page,error_out=False)
    return render_template('view.html',posts=posts)

@main.route('/active_user', methods=['GET'])
@login_required
def active_user():
    return render_template('active_user.html')
