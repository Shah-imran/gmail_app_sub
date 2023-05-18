import base64
from functools import wraps
from flask import flash, request, Response
from flask_login import current_user, login_required
from app.auth.services import redirect_user, api_authentication


def roles_required(roles):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if current_user.role.name in roles:
                return f(*args, **kwargs)
            else:
                flash("Access Restricted")
                return redirect_user()
            
        return wrap

    return decorator


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or 'Basic ' not in auth:
            return authenticate()
        encoded_credentials = auth.replace('Basic ', '', 1)
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
        
        if api_authentication(username, password):
            return f(*args, **kwargs)
        
        return authenticate()
    
    return decorated


def login_or_basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return login_required(f)(*args, **kwargs)
        else:
            auth = request.headers.get('Authorization')
            if auth and 'Basic ' in auth:
                return basic_auth_required(f)(*args, **kwargs)
            else:
                return authenticate()
    return decorated