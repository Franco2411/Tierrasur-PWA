from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort
from tierrasur.auth import required_login
from tierrasur.db import get_db
from datetime import datetime
import logging

bp = Blueprint('home', __name__)

logging.basicConfig(level=logging.DEBUG)

@bp.route('/', methods=['POST', 'GET'])
@required_login
def index():
    db, c = get_db()
    c.execute('select * from campos order by id asc')
    campos_list = c.fetchall()
    error = None
    c.execute('select * from activity order by id1 asc')
    actividad_list = c.fetchall()       
    
    return render_template('base.html', campos_list=campos_list, actividad_list=actividad_list)

@bp.route('/api/save_data', methods=['POST'])
def save_data():
    db, c = get_db()
    data = request.get_json()

    try:
        fecha = datetime.now()
        usuario = g.user['nick']
        campa = '24/25'

        # Inserto la orden
        c.execute(
                'insert into ordenes (creado_por, fecha) values (%s, %s)', (usuario, fecha)
            )
        order_id = c.lastrowid
        logging.debug(f'La orden fue insertada con el id: {order_id}')

        # Inserto los registros asociados
        for item in data['items']:
            c.execute(
                    'insert into hoja_tareas (up, lote, actividad, fecha, cant, detalle, codigo, campa, nro_c, precio) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (item['up'], item['lote'], item['actividad'], fecha, item['cant'], item['insumo'], item['tipo'], campa, order_id, item['precio'])
                )
        db.commit()
        return jsonify({'success': True, 'order_id': order_id})
    except Exception as e:
        db.rollback()
        #error = f'Error {e}'
        return jsonify({'success': False, 'error': str(e)})


@bp.route('/order_success/<int:order_id>')
@required_login
def order_success(order_id):
    return f'La orden n° {order_id} fue creada con exito'

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