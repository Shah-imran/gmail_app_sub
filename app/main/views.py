from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import inspect
from flask import render_template, redirect, request, url_for, flash, current_app, jsonify
from app.auth.services import (
    create_a_user, 
    reset_password, 
    redirect_user, 
    cross_auth_for_server,
    get_user_by_email,
    get_user_by_username
    
)
from app.main import services
from app.main import main
from app.main.forms import UserCreationForm, ServerCreationForm, PasswordResetForm
from .. import config, db
from app.models import User, Role
from app.utils import roles_required, basic_auth_required, login_or_basic_auth_required
from app.email import send_email
from app.settings import USER_CREATION_MAIL_SUBJECT


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
        return redirect_user()
    return redirect(url_for('auth.login'))


@main.route('/all-users', methods=['GET', 'POST'])
@login_required
@roles_required(['Admin'])
def all_users():
    form = UserCreationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = create_a_user(form)

        send_email(user.email, USER_CREATION_MAIL_SUBJECT, 'mail/account_creation', user=user, form=form)
        
        flash('Successfully Created')
    else:
        if request.method != 'GET':
            flash("Form validation failed.")

    return render_template('all_users.html', form=form)


@main.route('/all-users/get-list', methods=['GET'])
@login_required
@roles_required(['Admin'])
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
@roles_required(['Admin'])
def change_user_status(flag, id):
    if not services.change_active_status(flag, id):
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({"message": "Status Changed"}), 200


@main.route('/delete-user/<int:id>', methods=['DELETE'])
@login_required
@roles_required(['Admin'])
def delete_user(id):
    if not services.delete_user(id):
        return jsonify({'message': 'User not found!'}), 401

    return jsonify({"message": "User Deleted!"}), 200


@main.route('/servers', methods=['GET', 'POST'])
@login_required
@roles_required(['Admin'])
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
@roles_required(['Admin'])
def get_all_servers(): 
    servers = services.get_all_servers()
    
    if not servers:
        return jsonify({"message": "No results"}), 404
    
    return jsonify({
        "message": "ok",
        "data": servers
    }), 200


@main.route('/change-user-for-server/<int:server_id>/<string:user_id>', methods=['POST'])
@login_required
@roles_required(['Admin'])
def change_user_for_server(server_id , user_id): 
    user_id = int(user_id)
    if not services.change_user_for_server(server_id , user_id):
        return jsonify({"message": "Server not found"}), 404
    
    return jsonify({"message": "User Changed"}), 200


@main.route('/change-sub-for-server/<int:server_id>/<string:sub_id>', methods=['POST'])
@login_required
@roles_required(['Admin'])
def change_sub_for_server(server_id , sub_id): 
    sub_id = int(sub_id)
    if not services.change_sub_for_server(server_id , sub_id):
        return jsonify({"message": "Server not found"}), 404
    
    return jsonify({"message": "Subscription Changed"}), 200


@main.route('/change-server-status/<string:flag>/<int:id>', methods=['POST'])
@login_required
@roles_required(['Admin'])
def change_server_status(flag, id):
    if not services.change_server_active_status(flag, id):
        return jsonify({"message": "Server not found"}), 404
    
    return jsonify({"message": "Status Changed"}), 200


@main.route('/change-server-sub-date/<int:id>/<string:sub_end_date>', methods=['POST'])
@login_required
@roles_required(['Admin'])
def change_server_sub_date(id, sub_end_date):
    if not services.change_server_sub_date(id, sub_end_date):
        return jsonify({"message": "Server not found"}), 404
    
    return jsonify({"message": "Subscription date updated"}), 200


@main.route('/delete-server/<int:id>', methods=['DELETE'])
@login_required
@roles_required(['Admin'])
def delete_server(id):
    if not services.delete_server(id):
        return jsonify({'message': 'Server not found!'}), 401

    return jsonify({"message": "Server Deleted!"}), 200


@main.route('/subscription/get-all', methods=['GET'])
@login_required
@roles_required(['Admin', 'User'])
def get_all_subs(): 
    all_subs = services.get_all_subs()
    
    if not all_subs:
        return jsonify({"message": "No results"}), 404
    
    return jsonify({
        "message": "ok",
        "data": all_subs
    }), 200


@main.route('/packages', methods=['GET'])
@login_required
@roles_required(['Admin', 'User'])
def packages():
    return render_template('packages.html')


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
@roles_required(['User'])
def dashboard():
    form = PasswordResetForm(request.form)

    if request.method == 'POST' and form.validate():
        user = reset_password(form)

        flash('Password changed successfully.')
    else:
        if request.method != 'GET':
            flash("Form validation failed.")

    return render_template('dashboard.html', form=form)


@main.route('/get-user-server-sub-info', methods=['GET'])
@login_required
@roles_required(['Admin', 'User'])
def get_user_server_sub_info():
    user_data = services.get_user_server_sub_info(current_user.get_id())
    
    if not user_data:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "message": "ok",
        "data": user_data
    }), 200


@main.route('/api/get-user-server-sub-info/<string:username_or_password>', methods=['GET'])
@basic_auth_required
@roles_required(['Api'])
def get_user_server_sub_info_api(username_or_password):
    user: User = get_user_by_username(username_or_password) \
                    or get_user_by_email(username_or_password)
    
    user_data = services.get_user_server_sub_info(user.id)
    
    if not user_data:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "message": "ok",
        "data": user_data
    }), 200


@main.route('/api/check-user-password-server/<string:username_or_email>/<string:password>', methods=['GET'])
@basic_auth_required
@roles_required(['Api'])
def check_user_password_server(username_or_email, password):

    if not cross_auth_for_server(username_or_email, password):
        return jsonify({"message": "User Password Mismatch"}), 404
    
    return jsonify({ "message": "Success" }), 200

