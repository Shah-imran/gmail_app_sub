from flask import render_template, redirect, request, url_for, flash
from . import auth
from ..models import User


@auth.route('/', methods=['POST'])
def login():
    print("posted")

