from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('application', __name__)

@bp.route('/')
def index():
    return render_template('application/index.html')

@bp.route('/dataset')
def dataset():
    return render_template('application/dataset.html')

@bp.route('/login')
def login():
    return render_template('application/login.html')