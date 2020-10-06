from flask import render_template, redirect, request, url_for, flash
from . import verify
from ..models import User, Subscriber
from .. import db


@verify.route('/', methods=['POST'])
def index():
    print(request.json)
    return "ok"

@verify.route('/register', methods=['POST'])
def register():
    # print(request.json)
    if not Subscriber.query.filter_by(email=request.json['email']).first():
        sub = Subscriber(email=request.json['email'],
                        password=request.json['password'],
                        machine_uuid=request.json['machine_uuid'],
                        processor_id=request.json['processor_id']
                        )
        db.session.add(sub)
        db.session.commit()
        return "Successfully Registered"
    else:
        return "Already exists"

@verify.route('/login', methods=['POST'])
def login():
    # print(request.json)
    sub = Subscriber.query.filter_by(email=request.json['email']).first()
    if sub:
        sub = Subscriber(email=request.json['email'],
                        password=request.json['password'],
                        machine_uuid=request.json['machine_uuid'],
                        processor_id=request.json['processor_id']
                        )
        db.session.add(sub)
        db.session.commit()
        return "Successfully Registered"
    else:
        return "Not registered"

