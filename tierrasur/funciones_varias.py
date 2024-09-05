import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from flask import current_app, g

def envio_mail(usuario, email, contrasenia):
    # Cargo las variables de entorno
    sg_key = current_app.config['SG_KEY']

    message = Mail(
        from_email='tierrasur.sa2020@gmail.com',
        to_emails='fra98nba@gmail.com',
        subject='El usuario {} solicita acceso a Tierrasur-Web'.format(usuario),
        html_content='<h2>Solicitud de acceso a la plataforma</h2><div><p>Datos del usuario solicitante:</p><ul><li>Nombre: {} </li><li>Email: {} </li><li>Contraseña: {} </li></ul></div>'.format(usuario, email, contrasenia)
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
        