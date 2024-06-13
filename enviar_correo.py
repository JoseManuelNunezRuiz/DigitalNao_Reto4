import sys
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
from datetime import datetime
import smtplib

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Acuerdo de Confidencialidad', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def generar_pdf(nombre, fecha, empresa="BrokerIA"):
    pdf = PDF()
    pdf.add_page()

    title = "Acuerdo de Confidencialidad"
    body = f"""
    Este Acuerdo de Confidencialidad ("Acuerdo") se celebra entre {nombre} y {empresa}, con fecha de {fecha}.
    
    1. Definición de Información Confidencial. A los efectos del presente Acuerdo, "Información Confidencial" incluirá toda información o datos de naturaleza confidencial que sean divulgados por una de las partes a la otra.
    
    2. Obligaciones de Confidencialidad. La parte receptora se compromete a mantener la confidencialidad de la Información Confidencial y no divulgarla a terceros sin el consentimiento previo por escrito de la parte divulgadora.
    
    3. Duración. Este Acuerdo será efectivo a partir de la fecha mencionada anteriormente y permanecerá en vigor durante un período de 6 meses a partir de esa fecha.
    
    Firmado,


    {empresa}
    """

    pdf.chapter_title(title)
    pdf.chapter_body(body)

    filename = f"acuerdo_confidencialidad_{nombre.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

class EmailSender:
    def __init__(self, remitente, contrasena):
        self.remitente = remitente
        self.contrasena = contrasena

    def enviar_correo(self, destinatario, asunto, cuerpo, adjunto=None):
        msg = MIMEMultipart()
        msg['From'] = self.remitente
        msg['To'] = destinatario
        msg['Subject'] = asunto

        msg.attach(MIMEText(cuerpo, 'plain'))

        if adjunto:
            with open(adjunto, 'rb') as adjunto_archivo:
                parte = MIMEBase('application', 'octet-stream')
                parte.set_payload(adjunto_archivo.read())
                encoders.encode_base64(parte)
                parte.add_header('Content-Disposition', f'attachment; filename={adjunto}')
                msg.attach(parte)

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
                servidor.starttls()
                servidor.login(self.remitente, self.contrasena)
                texto = msg.as_string()
                servidor.sendmail(self.remitente, destinatario, texto)
                print(f'Correo enviado a {destinatario}')
        except Exception as e:
            print(f'Error al enviar correo a {destinatario}: {e}')

    def leer_correos(self, archivo_csv):
        with open(archivo_csv, mode='r', newline='') as archivo:
            lector = csv.DictReader(archivo)
            return [{'nombre': fila['nombre'], 'email': fila['email'], 'fecha_cumpleanos': fila['fecha_cumpleanos']} for fila in lector]

    def enviar_saludos(self, archivo_csv, asunto):
        correos = self.leer_correos(archivo_csv)
        mensaje_saludo = f"Hola {{nombre}}, ¡esperamos que tengas un gran inicio de semana!\n\nSaludos,\nBrokerIA"

        for correo in correos:
            cuerpo = mensaje_saludo.format(nombre=correo['nombre'])
            self.enviar_correo(correo['email'], asunto, cuerpo)

    def enviar_felicitaciones_cumpleanos(self, archivo_csv, asunto, template_html):
        fecha_actual = datetime.now().strftime("%d-%m")

        correos = self.leer_correos(archivo_csv)
        template = self.cargar_template(template_html)

        for correo in correos:
            fecha_cumpleanos = correo['fecha_cumpleanos']

            if fecha_cumpleanos == fecha_actual:
                cuerpo_html = template.replace('{{nombre}}', correo['nombre'])
                self.enviar_correo(correo['email'], asunto, cuerpo_html, adjunto=None)

    def enviar_acuerdo_confidencialidad(self, archivo_csv, remitente, contrasena):
        correos = self.leer_correos(archivo_csv)
        fecha_actual = datetime.now().strftime("%d-%m-%Y")

        for correo in correos:
            nombre = correo['nombre']
            email = correo['email']
            archivo_pdf = generar_pdf(nombre, fecha_actual)
            asunto = "Acuerdo de Confidencialidad"
            cuerpo = f"Hola {nombre}, adjunto encontrarás el acuerdo de confidencialidad. Por favor revisa y firma el documento.\n\nSaludos,\nBrokerIA"
            self.enviar_correo(email, asunto, cuerpo, adjunto=archivo_pdf)

    def cargar_template(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            return archivo.read()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python enviar_correo.py <accion>")
        sys.exit(1)

    accion = sys.argv[1]
    remitente = 'ing.josenruiz@gmail.com'
    contrasena = 'mi_pass'
    asunto_saludos = 'Saludos desde BrokerIA'
    asunto_felicitaciones = '¡Feliz Cumpleaños!'
    template_felicitaciones = 'felicitaciones.html'

    email_sender = EmailSender(remitente, contrasena)

    if accion == 'saludos':
        email_sender.enviar_saludos('correos.csv', asunto_saludos)
    elif accion == 'cumpleanos':
        email_sender.enviar_felicitaciones_cumpleanos('correos.csv', asunto_felicitaciones, template_felicitaciones)
    elif accion == 'acuerdo':
        email_sender.enviar_acuerdo_confidencialidad('correos.csv', remitente, contrasena)
    else:
        print(f"Acción '{accion}' no reconocida.")
