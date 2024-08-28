from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort
from tierrasur.auth import required_login
from tierrasur.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
@required_login
def index():
    db, c = get_db()
    c.execute('select * from campos order by id asc')
    campos_list = c.fetchall()

    c.execute('select * from activity order by id1 asc')
    actividad_list = c.fetchall()

    return render_template('base.html', campos_list=campos_list, actividad_list=actividad_list)


@bp.route('/combo_lotes', methods=['GET'])
@required_login
def combo_lotes():
    campos_id = request.args.get('campos_id')
    db, c = get_db()
    c.execute("select * from lotes where numcam = %s and campana='24/25'", (campos_id,))
    lotes_list = c.fetchall()

    return jsonify(lotes_list)

@bp.route('/combo_insumo_labor', methods=['GET'])
@required_login
def combo_insumo_labor():
    db, c = get_db()

    tabla_id = request.args.get('tabla_id')
    query = f'select * from {tabla_id}'
    c.execute(query)
    registros = c.fetchall()

    return jsonify(registros)