from flask import render_template, redirect, request, url_for, flash, current_app, jsonify
from app.auth.services import create_a_user
from app.main import services
from app.main import main
from app.main.forms import UserCreationForm, ServerCreationForm
from .. import config, db
from app.models import User, Role
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
        return redirect(url_for('main.all_users'))
    return redirect(url_for('auth.login'))


@main.route('/all-users', methods=['GET', 'POST'])
@login_required
def all_users():
    form = UserCreationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = create_a_user(form)
        
        flash('Successfully Created')
    else:
        if request.method != 'GET':
            flash("Form validation failed.")

    return render_template('all_users.html', form=form)


@main.route('/all-users/get-list', methods=['GET'])
@login_required
def get_all_users(): 
    all_users = services.get_all_users()
    
    if not all_users:
        return jsonify({"message": "No results"}), 404
    
    return jsonify({
        "message": "ok",
        "data": all_users
    }), 200


@main.route('/change-user-status/<string:flag>/<int:id>', methods=['POST'])
@login_required
def change_user_status(flag, id):
    if not services.change_active_status(flag, id):
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({"message": "Status Changed"}), 200


@main.route('/delete-user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    if not services.delete_user(id):
        return jsonify({'message': 'User not found!'}), 401

    return jsonify({"message": "User Deleted!"}), 200


@main.route('/servers', methods=['GET', 'POST'])
@login_required
def servers():
    form = ServerCreationForm(request.form)

    if request.method == 'POST' and form.validate():
        server = services.create_a_server(form)
        
        flash('Successfully Created a server')
    else:
        if request.method != 'GET':
            flash("Form validation failed.")

    return render_template('servers.html', form=form)


@main.route('/servers/get-all', methods=['GET'])
@login_required
def get_all_servers(): 
    servers = services.get_all_servers()
    
    if not servers:
        return jsonify({"message": "No results"}), 404
    
    return jsonify({
        "message": "ok",
        "data": servers
    }), 200


@main.route('/change-server-status/<string:flag>/<int:id>', methods=['POST'])
@login_required
def change_server_status(flag, id):
    if not services.change_server_active_status(flag, id):
        return jsonify({"message": "Server not found"}), 404
    
    return jsonify({"message": "Status Changed"}), 200


@main.route('/delete-server/<int:id>', methods=['DELETE'])
@login_required
def delete_server():
    if not services.delete_server(id):
        return jsonify({'message': 'Server not found!'}), 401

    return jsonify({"message": "Server Deleted!"}), 200


# @main.route('/active_user', methods=['GET'], defaults={"page": 1})
# @main.route('/active_user/<int:page>', methods=['GET'])
# @login_required
# def active_user(page):
#     per_page = current_app.config["PER_PAGE_PAGINATION"]
#     subscribers = db.session.query(Subscriber).filter_by(
#         active=True).paginate(page, per_page, error_out=False)
#     return render_template('active_user.html', subscribers=subscribers, page=page)


# @main.route('/active_users', methods=['GET'])
# @login_required
# def get_all_active_users():
#     subscribers: Subscriber = db.session.query(Subscriber).filter_by(
#         active=True).all()

#     if not subscribers:
#         return jsonify({"result": "No results"}), 404

#     data = []
#     for item in subscribers:

#         data.append({
#             "email": item.email,
#             "machine_uuid": item.machine_uuid,
#             "processor_id": item.processor_id,
#             "deactivate": {
#                 "id": item.id,
#                 "end_date": str(item.end_date)
#             },
#             "last_sign_in": str(item.last_sign_in),
#             "end_date": str(item.end_date)
#         })

#     return jsonify({
#         "result": "ok",
#         "data": data
#     }), 200

# @main.route('/activate_user/<string:end_date>/<int:id>', methods=['POST'])
# @login_required
# def activate_user(end_date, id):
#     sub = db.session.query(Subscriber).get(id)
#     if not sub:
#         return jsonify({'message': 'User not found!'}), 401
#     sub.end_date = datetime.strptime(end_date, '%Y-%m-%d')
#     sub.active = True

#     db.session.add(sub)
#     db.session.commit()
#     return jsonify({"message": "User Activated!"}), 200


# @main.route('/change_subscription/<string:end_date>/<int:id>', methods=['POST'])
# @login_required
# def change_subscription(end_date, id):
#     sub = db.session.query(Subscriber).get(id)
#     if not sub:
#         return jsonify({'message': 'User not found!'}), 401
#     sub.end_date = datetime.strptime(end_date, '%Y-%m-%d')
#     # print(sub.end_date)
#     db.session.add(sub)
#     db.session.commit()
#     return jsonify({"message": "Date Changed!"}), 200


# @main.route('/deactivate_user/<int:id>', methods=['POST'])
# @login_required
# def deactivate_user(id):
#     sub = db.session.query(Subscriber).get(id)
#     if not sub:
#         return jsonify({'message': 'User not found!'}), 401
#     sub.active = False
#     db.session.add(sub)
#     db.session.commit()
#     return jsonify({"message": "User deactivated!"}), 200
