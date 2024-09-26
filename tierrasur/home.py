from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort
from tierrasur.auth import required_login
from tierrasur.db import get_db
from datetime import datetime
import logging
from tierrasur.funciones_varias import anio_campania

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
        campa = anio_campania()

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

# Api para recuperar los registros hechos por un usuario
@bp.route('/api/get_registers', methods=['GET'])
def get_registers():
    db, c = get_db()
    data = request.get_json()
    error = None
    registros = []

    #id_usuario = g.user['nick']
    id_usuario = data.get('nick')
    fecha_inicio = datetime.strptime(data.get('fecha_inicio'), '%d/%m/%Y')
    fecha_final = datetime.strptime(data.get('fecha_final'), '%d/%m/%Y')
    logging.debug(f'Los datos enviados via api son id: {id_usuario}, fecha1: {fecha_inicio}, fecha2: {fecha_final}')

    if not id_usuario or not fecha_inicio or not fecha_final:
        error = 'Se tienen que completar todos los datos'
        return jsonify({'success': False, 'message': error})
    else:
        c.execute(
        'select * from ordenes where creado_por = %s and fecha between %s and %s', (id_usuario, fecha_inicio, fecha_final)
        )
        ordenes = c.fetchall()
        logging.debug(ordenes)

        if not ordenes:
            error = 'No existen registros para el rango de fechas especificado.'
            logging.debug('Entre al if donde no hay ordenes')
            return jsonify({'success': True, 'message': error})
        else:
            for orden in ordenes:
                nro_c = orden['id']
                logging.debug(f'El nro_c es: {nro_c}')
                c.execute(
                    'select * from hoja_tareas where nro_c = %s order by fecha desc', (nro_c,)
                )
                reg = c.fetchall()
                for r in reg:
                    reg_dic = {
                        'id': r['id'],
                        'up': r['up'],
                        'lote': r['lote'],
                        'actividad': r['actividad'],
                        'fecha': r['fecha'].isoformat(timespec='seconds'),
                        'cantidad': r['cant'],
                        'detalle': r['detalle'],
                        'codigo': r['codigo'],
                        'uta': r['uta'],
                        'restar': r['restar'],
                        'campania': r['campa'],
                        'pc': r['pc'],
                        'fechata': r['fechata'],
                        'nro_c': r['nro_c'],
                        'cplan': r['cplan'],
                        'borrador': r['borrador'],
                        'precio': r['precio']
                    }
                    registros.append(reg_dic)
            return jsonify({'success': True, 'data': registros})

    

