from functools import wraps
from flask import flash
from flask_login import current_user
from app.auth.services import redirect_user


def roles_required(role):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if current_user.role.name == role:
                return f(*args, **kwargs)
            else:
                flash("Access Restricted")

                return redirect_user()

        return wrap

    return decorator