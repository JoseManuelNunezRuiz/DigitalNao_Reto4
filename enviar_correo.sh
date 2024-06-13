#!/bin/bash

# Función para enviar saludos cada lunes a las 8:00 AM
function enviar_saludos() {
    python3 enviar_correo.py saludos
}

# Función para enviar felicitaciones por cumpleaños todos los días a las 8:00 AM
function enviar_felicitaciones_cumpleanos() {
    python3 enviar_correo.py cumpleanos
}

# Función para enviar PDFs personalizados cada seis meses
function enviar_pdfs() {
    python3 enviar_correo.py acuerdo
}

# Configurar la tarea programada para enviar saludos cada lunes a las 8:00 AM
schedule_saludos="0 8 * * 1"
croncmd_saludos="enviar_saludos"
cronjob_saludos="$schedule_saludos $croncmd_saludos"
(crontab -l | grep -v -F "$croncmd_saludos"; echo "$cronjob_saludos") | crontab -

# Configurar la tarea programada para enviar felicitaciones por cumpleaños todos los días a las 8:00 AM
schedule_felicitaciones="0 8 * * *"
croncmd_felicitaciones="enviar_felicitaciones_cumpleanos"
cronjob_felicitaciones="$schedule_felicitaciones $croncmd_felicitaciones"
(crontab -l | grep -v -F "$croncmd_felicitaciones"; echo "$cronjob_felicitaciones") | crontab -

# Configurar la tarea programada para enviar PDFs cada seis meses (1 de enero y 1 de julio a las 8:00 AM)
schedule_pdfs="0 8 1 1,7 *"
croncmd_pdfs="enviar_pdfs"
cronjob_pdfs="$schedule_pdfs $croncmd_pdfs"
(crontab -l | grep -v -F "$croncmd_pdfs"; echo "$cronjob_pdfs") | crontab -

# Salida de confirmación
echo "Configuración de cron completada para enviar saludos los lunes, felicitaciones diarias por cumpleaños y PDFs cada seis meses."

# Descargar el script de Python de GitHub (opcional, si el script no está localmente)
curl -O https://raw.githubusercontent.com/JoseManuelNunezRuiz/DigitalNao_Reto4/main/enviar_correo.py

# Ejecutar el script de Python que envía los PDFs, saludos y felicitaciones por correo
python3 enviar_correo.py
