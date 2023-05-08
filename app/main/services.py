from flask import jsonify

from .. import config, db
from app.models import User, Role


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

