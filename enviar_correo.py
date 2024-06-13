import sys
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class EmailSender:
    def __init__(self, remitente, contrasena):
        self.remitente = remitente
        self.contrasena = contrasena

    def leer_correos(self, archivo_csv):
        with open(archivo_csv, mode='r', newline='') as archivo:
            lector = csv.DictReader(archivo)
            return [{'nombre': fila['nombre'], 'email': fila['email'], 'mensaje': fila['mensaje'], 'fecha_cumpleanos': fila['fecha_cumpleanos']} for fila in lector]

    def cargar_template(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            return archivo.read()

    def enviar_correo(self, destinatario, asunto, cuerpo, formato='plain'):
        msg = MIMEMultipart()
        msg['From'] = self.remitente
        msg['To'] = destinatario
        msg['Subject'] = asunto

        msg.attach(MIMEText(cuerpo, formato))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
                servidor.starttls()
                servidor.login(self.remitente, self.contrasena)
                texto = msg.as_string()
                servidor.sendmail(self.remitente, destinatario, texto)
                print(f'Correo enviado a {destinatario}')
        except Exception as e:
            print(f'Error al enviar correo a {destinatario}: {e}')

    def enviar_saludos(self, archivo_csv, asunto):
        correos = self.leer_correos(archivo_csv)

        for correo in correos:
            mensaje_saludo = f"{correo['mensaje']}\n\nSaludos,\nArturo Burela."
            self.enviar_correo(correo['email'], asunto, mensaje_saludo)

    def enviar_felicitaciones_cumpleanos(self, archivo_csv, asunto, template_html):
        fecha_actual = datetime.now().strftime("%d-%m")

        correos = self.leer_correos(archivo_csv)
        template = self.cargar_template(template_html)

        for correo in correos:
            fecha_cumpleanos = correo['fecha_cumpleanos']

            if fecha_cumpleanos == fecha_actual:
                cuerpo_html = template.replace('{{nombre}}', correo['nombre'])
                self.enviar_correo(correo['email'], asunto, cuerpo_html, formato='html')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python enviar_correo.py <accion>")
        sys.exit(1)

    accion = sys.argv[1]
    remitente = 'ing.josenruiz@gmail.com'
    contrasena = 'rwrg vxmi zzau mbti'
    asunto_saludos = 'Saludos desde BrokerIA'
    asunto_felicitaciones = '¡Feliz Cumpleaños!'
    template_felicitaciones = 'felicitaciones.html'

    email_sender = EmailSender(remitente, contrasena)

    if accion == 'saludos':
        email_sender.enviar_saludos('correos.csv', asunto_saludos)
    elif accion == 'cumpleanos':
        email_sender.enviar_felicitaciones_cumpleanos('correos.csv', asunto_felicitaciones, template_felicitaciones)
    else:
        print(f"Acción '{accion}' no reconocida.")
