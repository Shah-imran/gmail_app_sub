from flask import Blueprint

verify = Blueprint('auth', __name__)

from . import views
