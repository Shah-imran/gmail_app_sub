from flask import render_template, redirect, request, url_for, flash
from . import verify
from ..models import User, Subscriber
from .. import db
from datetime import datetime


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
        if (sub.email==request.json['email']
            and sub.verify_password(request.json['password'])==True
            and sub.machine_uuid==request.json['machine_uuid']
            and sub.processor_id==request.json['processor_id']):
            if not sub.active:
                return "Not activated yet. Contact Admin"
            if sub.end_date<datetime.utcnow().date():
                return "Subscription expired"


            sub.last_sign_in = datetime.utcnow()
            db.session.add(sub)
            db.session.commit()
            return "Success"
    else:
        return "Not registered"

