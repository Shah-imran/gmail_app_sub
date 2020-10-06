from flask import render_template, redirect, request, url_for, flash
from . import verify
from ..models import User, Subscriber


@verify.route('/', methods=['POST'])
def index():
    print(request.json)
    return "ok"

@verify.route('/register', methods=['POST'])
def register():
    print(request.json)
    if not Subscriber.query.filter_by(email=request.json['email']).first():
        sub = Subscriber(email=request.json['email'], password=)
    else:
        return "Already exists"

@verify.route('/login', methods=['POST'])
def login():
    print(request.json)
    return "ok"

