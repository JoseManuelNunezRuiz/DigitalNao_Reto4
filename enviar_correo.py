import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def leer_correo(archivocsv):
    with open(archivocsv, mode = 'r', newline = '') as archivo:
        lector = csv.DictReader(archivo)
        return [{'nombre' : fila['nombre'], 'email' : fila['email'], 'mensaje' : fila['mensaje']} for fila in lector]

def enviar_correo(destinatario, asunto, cuerpo, remitente, contrasena):
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remitente, contrasena)
            texto = msg.as_string()
            servidor.sendmail(remitente, destinatario, texto)
            print(f'Correo enviado a {destinatario}')
    except Exception as e:
        print(f'Error al enviar correo a {destinatario}: {e}')

def main():
    correos = leer_correo('correos.csv')
    remitente = 'ing.josenruiz@gmail.com'
    contrasena = 'rwrg vxmi zzau mbti'
    asunto = 'Saludos desde BrokerIA'

    for correo in correos:
        enviar_correo(correo['email'], asunto, correo['mensaje'], remitente, contrasena)

if __name__ == '__main__':
    main()