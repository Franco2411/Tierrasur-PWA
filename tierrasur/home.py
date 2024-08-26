from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from tierrasur.auth import required_login
from tierrasur.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
@required_login
def index():
    return render_template('base.html')