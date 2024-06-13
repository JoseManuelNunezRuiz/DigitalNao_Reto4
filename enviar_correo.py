import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self, remitente, contrasena):
        self.remitente = remitente
        self.contrasena = contrasena

    def leer_correos(self, archivo_csv):
        with open(archivo_csv, mode='r', newline='') as archivo:
            lector = csv.DictReader(archivo)
            return [{'nombre': fila['nombre'], 'email': fila['email'], 'mensaje': fila['mensaje']} for fila in lector]

    def cargar_template(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            return archivo.read()

    def enviar_correo(self, destinatario, asunto, cuerpo_html):
        msg = MIMEMultipart()
        msg['From'] = self.remitente
        msg['To'] = destinatario
        msg['Subject'] = asunto

        msg.attach(MIMEText(cuerpo_html, 'html'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
                servidor.starttls()
                servidor.login(self.remitente, self.contrasena)
                texto = msg.as_string()
                servidor.sendmail(self.remitente, destinatario, texto)
                print(f'Correo enviado a {destinatario}')
        except Exception as e:
            print(f'Error al enviar correo a {destinatario}: {e}')

    def enviar_felicitaciones(self, archivo_csv, template_html, asunto):
        correos = self.leer_correos(archivo_csv)
        template = self.cargar_template(template_html)

        for correo in correos:
            cuerpo_html = template.replace('{{nombre}}', correo['nombre'])
            self.enviar_correo(correo['email'], asunto, cuerpo_html)

if __name__ == '__main__':
    remitente = 'ing.josenruiz@gmail.com'
    contrasena = 'mi_pass'
    asunto = 'Saludos desde BrokerIA'

    email_sender = EmailSender(remitente, contrasena)
    email_sender.enviar_felicitaciones('correos.csv', 'felicitaciones.html', asunto)
