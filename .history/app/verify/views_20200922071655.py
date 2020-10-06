from flask import render_template, redirect, request, url_for, flash
from . import verify
from ..models import User


@verify.route('/', methods=['POST'])
def index():
    print(request.json)
    return "ok"

@verify.route('/register', methods=['POST'])
def register():
    print(request.json)
    return True

@verify.route('/login', methods=['POST'])
def login():
    print(request.json)
    return "ok"

