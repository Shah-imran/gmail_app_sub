from flask import render_template, redirect, request, url_for, flash, jsonify
from . import verify
from ..models import User, Subscriber, Version
from .. import db
from datetime import datetime


@verify.route('/', methods=['POST'])
def index():
    print(request.json)
    return "ok"

@verify.route('/register', methods=['POST'])
def register():
    # print(request.json)
    if not db.session.query(Subscriber).filter_by(email=request.json['email']).first():
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
    sub = db.session.query(Subscriber).filter_by(email=request.json['email']).first()
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
            return "Password or Machine doesn't match"
    else:
        return "Not registered"

@verify.route('/version', methods=['GET'])
def version():
    version = db.session.query(Version).order_by(Version.id.desc()).first()
    if version:
        return jsonify({
            "exists": True,
            "name": version.name,
            "link": version.link,
            "download": version.download,
            "size": version.size
        }), 200
    else:
        return jsonify({
            "exists": False,
        }), 200

@verify.route('/version', methods=['PUT'])
def version_create_or_update():
    data = request.get_json()
    print(data)
    if data:
        version = db.session.query(Version).filter(Version.name==data['name']).first()
        if version:
            version.link = data['link']
            version.size = data['size']
            version.download = 0
            db.session.add(version)
            db.session.commit()
            return jsonify({
                "status": "Version Updated"
            }), 200

        else:
            version = Version(
                                name=data['name'],
                                link=data['link'],
                                size=data['size'],
                                download=0
                            )
            db.session.add(version)
            db.session.commit()
            return jsonify({
                "status": "Version Added"
            }), 200
    else:
        return jsonify({
            "status": "NO DATA"
        }), 200


@verify.route('/version/<string:name>', methods=['POST'])
def version_check(name):
    version = db.session.query(Version).order_by(Version.id.desc()).first()
    if version:
        if version.name == name:
            return jsonify({
                "update_needed": False
            }), 200
        else:
            return jsonify({
                "update_needed": True,
                "name": version.name,
                "link": version.link,
                "size": version.size
            }), 200
    else:
        return jsonify({
                "update_needed": False
            }), 200

@verify.route('/version/download/<string:name>', methods=['POST'])
def download_check(name):
    if name:
        version = db.session.query(Version).order_by(Version.id.desc()).first()
        if version:
            version.download+=1
            db.session.add(version)
            db.session.commit()

    return jsonify({
        "message": "updated"
        }), 200
