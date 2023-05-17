from flask import jsonify
from datetime import datetime, timedelta
from .. import config, db
from app.models import User, Role, Server, Subscription
from app.settings import (
    DEFAULT_SUBSCRIPTION_ID, 
    DEFAULT_TRIAL_DAYS,
    DEFAULT_SUBSCRIPTION_DURATION
)


def change_server_sub_date(server_id, sub_end_date):
    server: Server = db.session.query(Server).filter_by(id=server_id).first()

    if not server:
        return False
    
    server.sub_end_date = datetime.strptime(str(sub_end_date), '%Y-%m-%d')

    db.session.add(server)
    db.session.commit()

    return True

def change_sub_for_server(server_id , sub_id):
    server: Server = db.session.query(Server).filter_by(id=server_id).first()

    if not server:
        return False
    
    if sub_id == -1:
        server.subs_id = None
        server.sub_end_date = None
    else:
        server.subs_id = sub_id
        days_to_add = DEFAULT_TRIAL_DAYS if sub_id == DEFAULT_SUBSCRIPTION_ID \
                    else DEFAULT_SUBSCRIPTION_DURATION
        sub_end_date = datetime.utcnow().date() + timedelta(int(days_to_add))
        server.sub_end_date = datetime.strptime(str(sub_end_date), '%Y-%m-%d')

    db.session.add(server)
    db.session.commit()

    return True


def get_all_subs():
    subs: list[Subscription] = db.session.query(Subscription).all()

    all_subs = []
    for item in subs:
        all_subs.append({
            'id': item.id,
            'name': item.name,
            'device_count': item.device_count,
            'desciption': item.description,
            'time_created': str(item.time_created),
            'time_updated': item.time_updated
        })

    return all_subs

def delete_server(id):
    server: Server = db.session.query(Server).filter_by(id=id).first()

    if not server:
        return None
    
    db.session.delete(server)
    db.session.commit()

    return True


def change_server_active_status(flag, id):
    server: Server = db.session.query(Server).filter_by(id=id).first()

    if not server:
        return False
    
    if flag == 'activate':
        server.active = True
    else:
        server.active = False

    db.session.add(server)
    db.session.commit()

    return True


def change_user_for_server(server_id , user_id):
    server: Server = db.session.query(Server).filter_by(id=server_id).first()

    if not server:
        return False
    
    if user_id == -1:
        server.user_id = None
        server.assigned = False
        server.subs_id = None
    else:
        server.user_id = user_id
        
        change_sub_for_server(server_id, DEFAULT_SUBSCRIPTION_ID)

        server.assigned = True

    db.session.add(server)
    db.session.commit()

    return True


def create_a_server(form):
    server: Server = Server()
    server.ip_address = form.ip_address.data
    server.active = True
    server.description = form.description.data

    db.session.add(server)
    db.session.commit()

    return server


def get_all_servers():
    servers = db.session.query(Server).all()
    users = [ {'email': item['email'], 'id': item['active']['id']} for item in get_all_users() ]
    subs_list = [ 
        {'name': item['name'], 'id': item['id']} for item in get_all_subs() 
    ]
    
    all_servers = []
    for item in servers: 
        if item.user_id:
            user = db.session.query(User).filter_by(id=item.user_id).first()
        
        if  item.subs_id:
            subs_type = db.session.query(Subscription).filter_by(id=item.subs_id).first()

        all_servers.append(
            {
                'ip_address': item.ip_address,
                'time_created': str(item.time_created),
                'user': {
                    'server_id': item.id,
                    'id': item.user_id,
                    'username': user.username if item.user_id else None,
                    'email': user.email if item.user_id else None,
                    'all_users': users
                },
                'sub_type': {
                    'server_id': item.id,
                    'id': item.subs_id,
                    'name': subs_type.name if item.subs_id else None,
                    'all_subs': subs_list
                },
                'sub_end_date': {
                    'id': item.id,
                    'date': str(item.sub_end_date) if item.subs_id else None
                },
                'active': {
                    'active': item.active,
                    'id': item.id
                },
                'delete': {
                    'id': item.id
                },
                'description': item.description
            }
        )
        
    return all_servers


def get_one_server(ip_address):
    server = db.session.query(Server).filter_by(ip_address=ip_address).first()

    return server

 
def get_all_users():
    role: Role = db.session.query(Role).filter_by(name='User').first()
    users: User = db.session.query(User).filter_by(role_id=role.id).all()

    if not users:
        return None

    all_users = []
    for item in users:
        all_users.append(
                {
                    "email": item.email,
                    "username": item.username,
                    "time_created": str(item.time_created),
                    "last_login_time": str(item.last_sign_in),
                    "active": {
                        "active": item.active,
                        "id": item.id
                    },
                    "delete": {
                        "id": item.id
                    }
            }
        )

    return all_users


def change_active_status(flag, id):
    user: User = db.session.query(User).filter_by(id=id).first()

    if not user:
        return False
    
    if flag == 'activate':
        user.active = True
    else:
        user.active = False

    db.session.add(user)
    db.session.commit()

    return True


def delete_user(id):
    user: User = db.session.query(User).filter_by(id=id).first()

    if not user:
        return None
    
    db.session.delete(user)
    db.session.commit()

    return True

