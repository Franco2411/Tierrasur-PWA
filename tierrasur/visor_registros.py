from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify, send_file
)
from werkzeug.exceptions import abort
from tierrasur.auth import required_login
from tierrasur.db import get_db
from datetime import datetime
import logging
from tierrasur.funciones_varias import anio_campania, descargaExcel
from io import BytesIO
import pandas as pd
from xlsxwriter import Workbook

bp = Blueprint('visor_registros', __name__)

@bp.route('/get_registros', methods=['GET'])
@required_login
def get_registros():

    return render_template('visor_registros.html')

# Api para recuperar los registros hechos por un usuario
@bp.route('/api/get_registers', methods=['GET'])
def get_registers():
    db, c = get_db()
    #data = request.get_json()
    error = None
    registros = []

    id_usuario = g.user['nick']
    #id_usuario = data.get('nick')
    fecha_inicio = datetime.strptime(request.args.get('fecha1'), '%d/%m/%Y')
    fecha_final = datetime.strptime(request.args.get('fecha2'), '%d/%m/%Y')
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
            return jsonify({'success': True, 'message': error, 'data': registros})
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
                        'fecha': r['fecha'].isoformat(),
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

@bp.route('/api/download_excel', methods=['GET'])
@required_login
def download_excel():
    error = None
    id_usuario = g.user['nick']
    fecha_inicio = datetime.strptime(request.args.get('fecha1'), '%d/%m/%Y')
    fecha_final = datetime.strptime(request.args.get('fecha2'), '%d/%m/%Y')

    # Obtengo los registros
    registros = descargaExcel(id_usuario, fecha_inicio, fecha_final)
    if error is not None:
        return jsonify({'success': True, 'message': 'No existen registros para descargar', 'data': False})
    else:
        # Creo el excel en memoria
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        # Escribo los datos en el excel
        registros.to_excel(writer, index=False, sheet_name='Registros del dia')

        # Guardo el archivo
        writer.close()
        output.seek(0)

        # Pongo el nombre al archivo
        filename = f"registros_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

        # Retorno el archivo
        return send_file(output, 
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     download_name=filename,
                     as_attachment=True)