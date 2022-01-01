from flask import render_template, redirect, request, url_for, flash, current_app, jsonify
from . import main
from ..models import Subscriber
from .. import config, db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import inspect


def object_as_dict(obj):
    """[summary]
    Args:
        obj ([orm]): [description]
    Returns:
        list[dict]: [description]
    """
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.pending_request'))
    return redirect(url_for('auth.login'))


@main.route('/pending_request', methods=['GET'], defaults={"page": 1})
@main.route('/pending_request/<int:page>', methods=['GET'])
@login_required
def pending_request(page):
    per_page = current_app.config["PER_PAGE_PAGINATION"]

    subscribers = db.session.query(Subscriber).paginate(
        page, per_page, error_out=False)
    return render_template('pending_request.html', subscribers=subscribers, page=page)


@main.route('/pending_request/all-users', methods=['GET'])
@login_required
def get_all_users():
    subscribers: Subscriber = db.session.query(Subscriber).all()

    if not subscribers:
        return jsonify({"result": "No results"}), 404

    data = []
    for item in subscribers:
        # data.append(
        #     [
        #         item.email, 
        #         item.machine_uuid, 
        #         item.processor_id,
        #         item.active,
        #         True,
        #         item.id  
        #     ]
        # )

        data.append({
            "email": item.email,
            "machine_uuid": item.machine_uuid,
            "processor_id": item.processor_id,
            "active": {
                "active": item.active,
                "id": item.id
            },
            "delete": {
                "id": item.id
            }
        })

    return jsonify({
        "result": "ok",
        "data": data
    }), 200


@main.route('/active_user', methods=['GET'], defaults={"page": 1})
@main.route('/active_user/<int:page>', methods=['GET'])
@login_required
def active_user(page):
    per_page = current_app.config["PER_PAGE_PAGINATION"]
    subscribers = db.session.query(Subscriber).filter_by(
        active=True).paginate(page, per_page, error_out=False)
    return render_template('active_user.html', subscribers=subscribers, page=page)


@main.route('/activate_user/<string:end_date>/<int:id>', methods=['POST'])
@login_required
def activate_user(end_date, id):
    sub = db.session.query(Subscriber).get(id)
    if not sub:
        return jsonify({'message': 'User not found!'}), 401
    sub.end_date = datetime.strptime(end_date, '%Y-%m-%d')
    sub.active = True

    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "User Activated!"}), 200


@main.route('/change_subscription/<string:end_date>/<int:id>', methods=['POST'])
@login_required
def change_subscription(end_date, id):
    sub = db.session.query(Subscriber).get(id)
    if not sub:
        return jsonify({'message': 'User not found!'}), 401
    sub.end_date = datetime.strptime(end_date, '%Y-%m-%d')
    # print(sub.end_date)
    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "Date Changed!"}), 200


@main.route('/delete_user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    sub = db.session.query(Subscriber).get(id)
    if not sub:
        return jsonify({'message': 'User not found!'}), 401
    db.session.delete(sub)
    db.session.commit()
    return jsonify({"message": "User Deleted!"}), 200


@main.route('/deactivate_user/<int:id>', methods=['POST'])
@login_required
def deactivate_user(id):
    sub = db.session.query(Subscriber).get(id)
    if not sub:
        return jsonify({'message': 'User not found!'}), 401
    sub.active = False
    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "User deactivated!"}), 200
