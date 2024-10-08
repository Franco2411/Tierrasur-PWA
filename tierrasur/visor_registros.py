from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify, send_file
)
from werkzeug.exceptions import abort
from tierrasur.auth import required_login
from tierrasur.db import get_db
from datetime import datetime
import logging
from tierrasur.funciones_varias import anio_campania, descargaExcel, obtRegistros
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
    
    id_usuario = g.user['nick']
    #data = request.get_json()
    #id_usuario = data.get('nick')
    fecha_inicio = datetime.strptime(request.args.get('fecha1'), '%d/%m/%Y')
    fecha_final = datetime.strptime(request.args.get('fecha2'), '%d/%m/%Y')
    logging.debug(f'Los datos enviados via api son id: {id_usuario}, fecha1: {fecha_inicio}, fecha2: {fecha_final}')

    registros, error = obtRegistros(id_usuario, fecha_inicio, fecha_final)

    return jsonify({'success': True, 'data': registros, 'message': error})

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