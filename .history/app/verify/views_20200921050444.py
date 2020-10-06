from flask import render_template, redirect, request, url_for, flash
from . import verify
from ..models import User


@verify.route('/', methods=['POST'])
def index():
    print(request.get_json(force=True))
    return "ok"

