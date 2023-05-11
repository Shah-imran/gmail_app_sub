from flask import jsonify
from .. import config, db
from app.models import User, Role, Server


def create_a_server(form):
    server: Server = Server()
    server.ip_address = form.ip_address.data
    server.active = True
    server.description = form.description.data

    db.session.add(server)
    db.session.commit()

    return server

def get_all_servers():
    return True


def get_one_server(ip_address):
    try:
        server = db.session.query(Server).filter_by(ip_address=ip_address).first()
    except:
        import traceback
        print(traceback.format_exc(), ip_address)

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

