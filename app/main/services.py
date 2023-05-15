from flask import jsonify
from .. import config, db
from app.models import User, Role, Server, Subscription


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
                {'name': item.name, 'id': item.id} 
                for item in db.session.query(Subscription).all() 
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
                    'id': item.user_id,
                    'username': user.username if item.user_id else None,
                    'email': user.email if item.user_id else None,
                    'all_users': users
                },
                'sub_type': {
                    'id': item.subs_id,
                    'name': subs_type if item.subs_id else None,
                    'all_subs': subs_list
                },
                'sub_end_date': str(item.sub_end_date) if item.subs_id else None,
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
        print(all_servers)
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

