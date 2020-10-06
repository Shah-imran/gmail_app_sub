from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/pending_request',methods=['GET'])
def pending_request():
    return render_template('index.html')

