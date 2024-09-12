import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from flask import current_app, g
from tierrasur.db import get_db
from datetime import datetime



def envio_mail(usuario, nombre, contrasenia):
    # Cargo las variables de entorno
    sg_key = current_app.config['SG_KEY']
    to_emm = consulta_emails()

    message = Mail(
        from_email='tierrasur.sa2020@gmail.com',
        to_emails=to_emm,
        subject='El usuario {} solicita acceso a Tierrasur-Web'.format(usuario),
        html_content='<h2>Solicitud de acceso a la plataforma</h2><div><p>Datos del usuario solicitante:</p><ul><li>Nombre: {} </li><li>Email: {} </li><li>Contraseña: {} </li></ul></div>'.format(usuario, nombre, contrasenia)
    )

    try:
        sg = SendGridAPIClient(sg_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print('Mail enviado con exito')
    except Exception as e:
        print('Ha ocurrido un error.')
        print(e.message)


def consulta_emails():
    lista_emails = []

    db, c = get_db()
    c.execute(
        'select email from mails'
    )
    cc = c.fetchall()
    if cc is None:
        #lista_emails.append('hda54software@gmail.com')
        print(f'La lista esta vacia parece ser: {cc}')
    else:    
        for item in cc:
            lista_emails.append(item['email'])
    return lista_emails


def anio_campania():
    hoy = datetime.now()
    dia = hoy.day
    mes = hoy.month
    anio = hoy.year

    campania = None

    if (dia <= 31 and mes <= 5):
        anio_anterior = hoy.strftime("%y")  # Año anterior en formato de dos dígitos
        anio_actual = (hoy.year - 1) % 100  # Restando 1 al año actual y formateando
        campania = f'{anio_actual:02}/{anio % 100:02}'  # Ambos años con dos dígitos
    else:
        anio_siguiente = (anio + 1) % 100  # Año siguiente en formato de dos dígitos
        campania = f'{anio % 100:02}/{anio_siguiente:02}'

    return campania
